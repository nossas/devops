from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from ..forms import EtcdKeyValueForm
from ..services.etcd_client import etcd_client


etcd_routes = Blueprint("etcd", __name__, url_prefix="/etcd")


@etcd_routes.route("/", methods=["GET", "POST"])
@login_required
def list_keys():
    form = EtcdKeyValueForm()

    if form.validate_on_submit():
        etcd_client.put(form.data.get("key"), form.data.get("value"))
        return redirect(url_for("etcd.list_keys"))

    result = []

    for value, metadata in etcd_client.get_prefix("traefik"):
        result.append(dict(
            key=metadata.key.decode('utf-8'),
            value=value.decode('utf-8')
        ))
    
    return render_template("etcd.html", items=result, form=form)


@etcd_routes.route("/delete", methods=["POST"])
@login_required
def delete_key():
    key = request.form.get("key")
    etcd_client.delete(key)

    return redirect(url_for("etcd.list_keys"))