import etcd3

etcd_client = etcd3.client(host='localhost', port=2379)


def get_service(domain_name):
    router_name = domain_name.replace(".", "-")

    result = []
    etcd_prefix_key = f"traefik/http/routers/{router_name}"

    for value, metadata in etcd_client.get_prefix(etcd_prefix_key):
        result.append(dict(
            key=metadata.key.decode('utf-8'),
            value=value.decode('utf-8')
        ))
    
    return result