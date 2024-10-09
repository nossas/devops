from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required

# import requests

from ..extensions import db
from ..models import Domain, Site
from ..forms import DomainForm, SiteForm
from ..services.etcd_client import get_service
from ..services.route53 import (
    route53,
    check_domain_configuration,
    is_domain_active,
    get_public_ip,
)

main_routes = Blueprint("main", __name__)


@main_routes.route("/complete", methods=["GET", "POST"])
@login_required
def complete():
    form = DomainForm()

    if form.validate_on_submit():
        values = {
            "name": form.name.data,
            "purchase_at": form.purchase_at.data,
            "expired_at": form.expired_at.data,
            # "external_id": form.external_id.data,
        }
        new_domain = Domain(**values)
        db.session.add(new_domain)
        db.session.commit()
        return redirect(url_for("main.index"))

    public_ip = get_public_ip()
    domains = []
    for domain in Domain.query.all():
        domains.append(
            dict(
                name=domain.name,
                is_active=is_domain_active(domain.name),
                is_route53=check_domain_configuration(domain.name, public_ip=public_ip),
                traefik_rules=get_service(domain.name),
            )
        )

    return render_template(
        "complete.html", domains=domains, form=form, public_ip=public_ip
    )


# @main_routes.route("/", methods=["GET", "POST"])
# @login_required
# def index():
#     form = SiteForm()

#     if form.validate_on_submit():
#         values = {"name": form.name.data, "community_id": form.community_id.data}

#         new_site = Site(**values)
#         db.session.add(new_site)
#         db.session.commit()

#         return redirect(url_for("main.index"))

#     return render_template("index.html", sites=Site.query.all(), form=form)


# @main_routes.route("/sites/<site_id>", methods=["GET", "POST"])
# def site_detail(site_id):
#     site = Site.query.get(site_id)

#     form = DomainForm()

#     if form.validate_on_submit():
#         values = {
#             "name": form.name.data,
#             "purchase_at": form.purchase_at.data,
#             "expired_at": form.expired_at.data,
#             "has_manage_dns": form.has_manage_dns.data,
#             "site": site
#         }
#         new_domain = Domain(**values)

#         if new_domain.has_manage_dns:
#             # Criar registro no Route53 pois nossa aplicação irá gerenciar
#             # esse domínio
            
#             response = route53.create_hosted_zone(
#                 Name=new_domain.name,
#                 CallerReference=str(hash(new_domain.name)),  # Referência única (pode ser UUID)
#             )

#             # Adiciona a tag com o identificador externo à Hosted Zone
#             zone_id = response["HostedZone"]["Id"]

#             # Update on Domain HostedZoneId
#             new_domain.hosted_zone_id = zone_id
#             db.session.add(new_domain)
#             db.session.commit()

#             # Atualiza Route53 com tags referentes Domain.id and Site.community_id
#             route53.change_tags_for_resource(
#                 ResourceType="hostedzone",
#                 ResourceId=zone_id.split("/")[-1],  # Apenas a parte final do ID
#                 AddTags=[
#                     # Tag usada para garantir dupla checagem de domínio / zona de hospedagem
#                     {"Key": "ExternalIdentifier", "Value": str(new_domain.id)},
#                     # Tag usada para agrupar domínios por Grupo / Comunidade
#                     {"Key": "GroupExternalIdentifier", "Value": str(site.community_id)}
#                 ],
#             )
#         else:
#             db.session.add(new_domain)
#             db.session.commit()

#         return redirect(url_for("main.site_detail", site_id=site_id))

#     return render_template(
#         "sites/detail.html",
#         site=site,
#         domains=Domain.query.filter_by(site_id=site.id),
#         form=form,
#     )


@main_routes.route("/domains/<domain_id>/delete", methods=["POST"])
def domain_delete(domain_id):
    site_id = request.form["site_id"]
    # Delete domain
    domain = Domain.query.get(domain_id)
    db.session.delete(domain)
    db.session.commit()

    return redirect(url_for("main.site_detail", site_id=site_id))