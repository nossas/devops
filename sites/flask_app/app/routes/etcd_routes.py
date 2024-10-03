from flask import Blueprint, render_template

from ..services.etcd_client import etcd_client


etcd_routes = Blueprint("etcd", __name__, url_prefix="/etcd")


@etcd_routes.route("/")
def list_keys():
    result = []

    for value, metadata in etcd_client.get_prefix("/traefik"):
        result.append(dict(
            key=metadata.key.decode('utf-8'),
            value=value.decode('utf-8')
        ))

    print(f"RESULT: {result}")
    
    return render_template("etcd.html", items=result)
