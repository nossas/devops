from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required

from ..extensions import db
from ..forms import SiteForm, DomainForm, RecordSetForm
from ..models import Site, Domain
from ..services.route53 import route53, get_public_ip


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    Listagem e Cadastro de Sites.
    """
    form = SiteForm()
    if form.validate_on_submit():
        values = {"name": form.name.data, "community_id": form.community_id.data}

        # Adiciona Site ao banco de dados
        new_site = Site(**values)
        db.session.add(new_site)
        db.session.commit()

        # Redireciona para si mesmo, agora abrindo com o metodo GET e com a listagem de Sites
        # atualizada.
        return redirect(url_for("dashboard.index"))

    return render_template("dashboard/index.html", sites=Site.query.all(), form=form)


@dashboard.route("/sites/<site_id>", methods=["GET", "POST"])
@login_required
def site_detail(site_id):
    """
    Detalhamento do Site, Listagem e Cadastro de Domínios.
    """
    site = Site.query.get(site_id)

    form = DomainForm()
    if form.validate_on_submit():
        values = {
            "name": form.name.data,
            "purchase_at": form.purchase_at.data,
            "expired_at": form.expired_at.data,
            "has_manage_dns": form.has_manage_dns.data,
            "site": site,
        }
        # Adiciona Domínio ao banco de dados
        new_domain = Domain(**values)

        if not new_domain.has_manage_dns:
            # Se esse domínio não deve ser gerenciado pelo aplicativo, apenas salva no banco
            # de dados para possibilitar o histórico das informações.
            db.session.add(new_domain)
            db.session.commit()
        else:
            # Se esse domínio deve ser gerenciado pelo aplicativo é criada então uma zona de
            # hospedagem no Route53 para que o usuário possa apontar as configurações do seu
            # domínio para o nosso servidor DNS, usando os NS (Name Servers)

            response = route53.create_hosted_zone(
                Name=new_domain.name,
                CallerReference=str(
                    hash(new_domain.name)
                ),  # Referência única (pode ser UUID)
            )

            # Armazena o identificador no Zona de Hospedagem no Domínio
            new_domain.hosted_zone_id = response["HostedZone"]["Id"]
            db.session.add(new_domain)
            db.session.commit()

            # Atualiza Route53 com tags para identificação do Domínio (Local) e da Comunidade (BONDE).
            route53.change_tags_for_resource(
                ResourceType="hostedzone",
                # Apenas a parte final do ID
                ResourceId=new_domain.hosted_zone_id.split("/")[-1],
                AddTags=[
                    # Tag usada para garantir dupla checagem de domínio / zona de hospedagem
                    {"Key": "ExternalIdentifier", "Value": str(new_domain.id)},
                    # Tag usada para agrupar domínios por Grupo / Comunidade
                    {"Key": "GroupExternalIdentifier", "Value": str(site.community_id)},
                ],
            )

        # Ao finalizar o processamento do formulário redireciona para si mesmo.
        # Carregando novamente a Listagem de Domínios.
        return redirect(url_for("dashboard.site_detail", site_id=site_id))

    # Renderiza o template com a Listagem de Domínios por Site
    return render_template(
        "dashboard/site_detail.html",
        site=site,
        domains=Domain.query.filter_by(site_id=site.id),
        form=form,
    )


@dashboard.route("/domains/<domain_id>", methods=["GET", "POST"])
@login_required
def domain_detail(domain_id):
    """
    Detalhamento do Domínio, Listagem e Cadastro dos Registros (Route53)
    """
    zone = None
    domain = Domain.query.get(domain_id)

    # O public_ip será útil para informar ao usuário qual IP ele deve usar para que o endereço
    # responda ao nosso Servidor.
    #
    # Caso o domínio não seja gerenciado pelo aplicativo, iremos informar ao usuário
    # para configurar o Registro do tipo A com o public_ip onde esse domínio está sendo gerenciado
    context = {"public_ip": get_public_ip(), "domain": domain}

    if domain.has_manage_dns:
        # Se o domínio é gerenciado pelo aplicativo, devemos fazer uma série de verificações
        # para garantir que iremos trabalhar a manutenção da Zona de Hospedagem correta.

        if not domain.hosted_zone_id:
            # Precisamos garantir que exista um hosted_zone_id relacionado esse valor deveria existir,
            # pois ele é adicionado assim que criamos um Domínio no aplicativo, porém podemos ter
            # criado o Domínio fora do aplicativo por algum motivo, então vamos verificar no Route53
            # se já existe algo criado com referência ao nosso Domínio.

            # Obter todas as Hosted Zones
            response = route53.list_hosted_zones()
            hosted_zones = response.get("HostedZones", [])

            # Listar de Zonas de Hospedagem que correspondem ao identificador externo
            for zone in hosted_zones:
                # Apenas a parte final do ID será usado para Listar as Tags
                zone_id = zone["Id"].split("/")[-1]

                # Obter as tags da zona de hospedagem
                tags_response = route53.list_tags_for_resource(
                    ResourceType="hostedzone", ResourceId=zone_id
                )
                tags = tags_response.get("ResourceTagSet", {}).get("Tags", [])

                # Verifica se a tag 'ExternalIdentifier' corresponde ao valor fornecido
                # que deveria ser o Id do Domínio
                for tag in tags:
                    if tag["Key"] == "ExternalIdentifier" and tag["Value"] == str(
                        domain.id
                    ):
                        # Salvar o hosted_zone_id caso ainda não tenha sido salvo no Domínio (Local),
                        # mas a tag esteja na Zona de Hospedagem do Route53
                        domain.hosted_zone_id = zone["Id"]
                        db.session.commit()
                        break

        # Valida o formulário caso tenham preenchido o formulário para criar um novo Registro
        # na Zona de Hospedagem
        form = RecordSetForm()
        if form.validate_on_submit():
            resource_record_set = {
                "Name": form.name.data,
                "Type": form.record_type.data,
                "ResourceRecords": [
                    {"Value": value} for value in form.value.data.split(",")
                ],
            }
            response = route53.change_resource_record_sets(
                HostedZoneId=domain.hosted_zone_id,
                ChangeBatch=dict(
                    Changes=[
                        dict(Action="CREATE", ResourceRecordSet=resource_record_set)
                    ]
                ),
            )

            # Ao finalizar o processamento do formulário redireciona para si mesmo.
            # Carregando novamente a Listagem de Regisros.
            return redirect(url_for("dashboard.domain_detail", domain_id=domain.id))

        # Adiciona o formulário ao contexto
        context.update({"form": form})

        # Busca pelos registros relacionados a Zona de Hospedagem
        response = route53.list_resource_record_sets(HostedZoneId=domain.hosted_zone_id)
        context.update({"records": response.get("ResourceRecordSets", [])})

    # Renderiza o template com a Listagem de Registros por Zona de Hospedagem
    return render_template("dashboard/domain_detail.html", **context)


@dashboard.route("/domains/<domain_id>/delete", methods=["POST"])
def domain_delete(domain_id):
    """
    Remover Domínio e seus relacionamentos
    """
    domain = Domain.query.get(domain_id)

    if domain.has_manage_dns:
        # Se o Domínio é gerenciado pelo aplicativo, então deve remover a
        # Zona de Hospedagem cadastrada no Route53
        #
        route53.delete_hosted_zone(Id=domain.hosted_zone_id)

    # O Domínio só é removido da base se a Zona de Hospedagem relacionada tiver
    # sido removida do Route53 também.
    db.session.delete(domain)
    db.session.commit()

    return redirect(url_for("dashboard.site_detail", site_id=domain.site_id))


@dashboard.route("/domains/<domain_id>/record/delete", methods=["POST"])
@login_required
def record_delete(domain_id):
    """
    Remover Registro do Route53 relacionado ao Domínio (Local)
    """
    domain = Domain.query.get(domain_id)

    resource_record_set = {
        "Name": request.form.get("name"),
        "Type": request.form.get("record_type"),
    }
    route53.change_resource_record_sets(
        HostedZoneId=domain.hosted_zone_id,
        ChangeBatch=dict(
            Changes=[dict(Action="DELETE", ResourceRecordSet=resource_record_set)]
        ),
    )

    return redirect(url_for("dashboard.domain_detail", domain_id=domain.id))
