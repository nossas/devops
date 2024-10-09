import boto3
import requests

route53 = boto3.client(
    'route53',
    endpoint_url='http://localhost:4566',  # LocalStack URL
    region_name='us-east-1',  # Região (pode ser qualquer uma)
    aws_access_key_id='fake-access-key',  # Chaves falsas para LocalStack
    aws_secret_access_key='fake-secret-key'
)


def check_domain_configuration(domain_name, public_ip="127.0.0.1"):
    """
    TODO: Configurar o apontamento dos IPs
    """
    hosted_zones = route53.list_hosted_zones_by_name(DNSName=domain_name)["HostedZones"]
    if len(hosted_zones) == 1:
        hosted_zone = hosted_zones[0]
        record_sets = route53.list_resource_record_sets(
            HostedZoneId=hosted_zone["Id"]
        )["ResourceRecordSets"]

        record_sets = list(filter(lambda x: x['Type'] == 'A', record_sets))
        if len(record_sets) > 0:
            for record in record_sets:
                for resource in record['ResourceRecords']:
                    if resource["Value"] == public_ip:
                        return True
    
    print(f"Configurações não encontradas para o domínio: {domain_name}")
    return False


def is_domain_active(domain):
    try:
        response = requests.get(f'http://{domain}', timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_public_ip():
    try:
        response = requests.get(f"https://checkip.amazonaws.com")
        response.raise_for_status()
        
        return response.text.strip()
    except requests.RequestException:
        return None


# def delete_records_by_domain(domain):
#     """
#     Listar Registros armazenados ao Route53 e remover eles para que seja possível
#     """
#     zone_id = request.form.get("zone_id")
#     resource_record_set = {
#         "Name": request.form.get("name"),
#         "Type": request.form.get("record_type"),
#     }
#     response = route53.change_resource_record_sets(
#         HostedZoneId=zone_id,
#         ChangeBatch=dict(
#             Changes=[dict(Action="DELETE", ResourceRecordSet=resource_record_set)]
#         ),
#     )
#     print(response)

#     return redirect(url_for("dns.list_records", zone_id=zone_id.split("/")[-1]))