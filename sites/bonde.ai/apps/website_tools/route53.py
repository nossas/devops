import boto3


route53 = boto3.client(
    'route53',
    endpoint_url='http://localhost:4566',  # LocalStack URL
    region_name='us-east-1',  # Região (pode ser qualquer uma)
    aws_access_key_id='fake-access-key',  # Chaves falsas para LocalStack
    aws_secret_access_key='fake-secret-key'
)