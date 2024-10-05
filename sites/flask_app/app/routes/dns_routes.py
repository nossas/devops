from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import urllib

from ..forms import RecordSetForm
from ..services.route53 import route53, check_domain_configuration, is_domain_active


dns_routes = Blueprint("dns", __name__, url_prefix="/dns")


@dns_routes.route("/", methods=["GET", "POST"])
@login_required
def list_hosted_zones():
    """Lista todas as Hosted Zones"""

    if (
        request.method == "POST"
        and "external_id" in request.form
        and request.form["external_id"]
    ):
        external_id = request.form["external_id"]  # Identificador externo para filtrar

        # Obtém todas as Hosted Zones
        response = route53.list_hosted_zones()
        hosted_zones = response.get("HostedZones", [])

        # Lista de Hosted Zones que correspondem ao identificador externo
        filtered_zones = []
        for zone in hosted_zones:
            zone_id = zone["Id"].split("/")[-1]  # Apenas a parte final do ID

            # Obtém as tags da zona
            tags_response = route53.list_tags_for_resource(
                ResourceType="hostedzone", ResourceId=zone_id
            )
            tags = tags_response.get("ResourceTagSet", {}).get("Tags", [])

            # Verifica se a tag 'ExternalIdentifier' corresponde ao valor fornecido
            for tag in tags:
                if tag["Key"] == "ExternalIdentifier" and tag["Value"] == external_id:
                    filtered_zones.append(zone)
                    break

        return render_template("zones.html", hosted_zones=filtered_zones)

    response = route53.list_hosted_zones()
    hosted_zones = response.get("HostedZones", [])

    # Codificar o ID das zonas para serem usados na URL
    for zone in hosted_zones:
        zone_id = zone["Id"].split("/")[-1]  # Pega apenas a parte final do ID
        zone["EncodedId"] = urllib.parse.quote(
            zone_id
        )  # Codifica o ID sem a parte '/hostedzone/'

    return render_template("zones.html", hosted_zones=hosted_zones)


@dns_routes.route("records/delete", methods=["POST"])
@login_required
def delete_record_set():
    zone_id = request.form.get("zone_id")
    resource_record_set = {
        "Name": request.form.get("name"),
        "Type": request.form.get("record_type"),
    }
    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch=dict(
            Changes=[dict(Action="DELETE", ResourceRecordSet=resource_record_set)]
        ),
    )
    print(response)

    return redirect(url_for("dns.list_records", zone_id=zone_id.split("/")[-1]))


@dns_routes.route("/records/<zone_id>", methods=["GET", "POST"])
@login_required
def list_records(zone_id):
    """Lista os registros DNS de uma Hosted Zone"""
    decoded_zone_id = urllib.parse.unquote(zone_id)
    full_zone_id = f"/hostedzone/{decoded_zone_id}"

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
            HostedZoneId=full_zone_id,
            ChangeBatch=dict(
                Changes=[dict(Action="CREATE", ResourceRecordSet=resource_record_set)]
            ),
        )
        print(response)
        return redirect(url_for("dns.list_records", zone_id=zone_id))

    # Obtém os registros DNS da Hosted Zone
    response = route53.list_resource_record_sets(HostedZoneId=full_zone_id)
    records = response.get("ResourceRecordSets", [])

    return render_template(
        "records.html", records=records, form=form, zone_id=full_zone_id
    )


@dns_routes.route("/create", methods=["POST"])
@login_required
def create_hosted_zone():
    """Cria uma nova Hosted Zone"""
    zone_name = request.form["zone_name"]  # Obtém o nome da zona do formulário
    external_id = request.form[
        "external_id"
    ]  # Identificador externo, por exemplo 'project_id'

    # Cria a Hosted Zone no Route53
    response = route53.create_hosted_zone(
        Name=zone_name,
        CallerReference=str(hash(zone_name)),  # Referência única (pode ser UUID)
    )

    # Adiciona a tag com o identificador externo à Hosted Zone
    zone_id = response["HostedZone"]["Id"]
    route53.change_tags_for_resource(
        ResourceType="hostedzone",
        ResourceId=zone_id.split("/")[-1],  # Apenas a parte final do ID
        AddTags=[{"Key": "ExternalIdentifier", "Value": external_id}],
    )

    return redirect(url_for("dns.list_hosted_zones"))


@dns_routes.route("/delete/<zone_id>", methods=["POST"])
@login_required
def delete_hosted_zone(zone_id):
    """Exclui uma Hosted Zone"""
    # Decodifica o ID da zona
    decoded_zone_id = urllib.parse.unquote(zone_id)

    # Exclui a Hosted Zone pelo ID completo ('/hostedzone/<ID>')
    full_zone_id = f"/hostedzone/{decoded_zone_id}"
    route53.delete_hosted_zone(Id=full_zone_id)

    return redirect(url_for("dns.list_hosted_zones"))
