from .route53 import route53
from .etcd_client import etcd_client


def update_or_create_dns_hosted_zone(sender, instance, **kwargs):
    response = route53.create_hosted_zone(
        Name=instance.name,
        CallerReference=str(
            hash(instance.name)
        ),  # Referência única (pode ser UUID)
    )

    # Armazena o identificador no Zona de Hospedagem no Domínio
    instance.hosted_zone_id = response["HostedZone"]["Id"]

    return instance


def delete_dns_hosted_zone(sender, instance, **kwargs):
    route53.delete_hosted_zone(Id=instance.hosted_zone_id)


def update_or_create_traefik_http_router(sender, instance, action, **kwargs):
    if action == "pre_add":
        schema = []
        schema.append(instance.get_m2m_rule(kwargs.get("pk_set")))
        schema.append(instance.get_service())
        schema.append(instance.get_entrypoints())
        schema.append(instance.get_tls())
        schema.append(instance.get_certresolver())

        for args in schema:
            etcd_client.put(*args)
        
        # print(schema)

        instance.schema_history = dict(schema)

def delete_traefik_http_router(sender, instance, **kwargs):
    etcd_client.delete_prefix(instance.prefix)