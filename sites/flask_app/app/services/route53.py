import boto3
import requests

route53 = boto3.client(
    'route53',
    endpoint_url='http://localstack:4566',  # LocalStack URL
    region_name='us-east-1',  # Região (pode ser qualquer uma)
    aws_access_key_id='fake-access-key',  # Chaves falsas para LocalStack
    aws_secret_access_key='fake-secret-key'
)


def check_domain_configuration(domain_name):
    hosted_zones = route53.list_hosted_zones()["HostedZones"]
    for zone in hosted_zones:
        if zone['Name'].rstrip('.') == domain_name:
            print(f"Configurações encontradas para o domínio: {domain_name}")
            return True
    
    print(f"Configurações não encontradas para o domínio: {domain_name}")
    return False


def is_domain_active(domain):
    try:
        response = requests.get(f'http://{domain}', timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False