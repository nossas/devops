from flask import Blueprint, render_template, url_for, redirect, request
import requests

from ..extensions import db
from ..models import Domain
from ..forms import DomainForm
from ..services.route53 import (
    check_domain_configuration,
    is_domain_active,
    get_public_ip,
)

main_routes = Blueprint("main", __name__)


@main_routes.route("/", methods=["GET", "POST"])
def index():
    form = DomainForm()

    if form.validate_on_submit():
        values = {
            "name": form.name.data,
            "purchase_at": form.purchase_at.data,
            "expired_at": form.expired_at.data,
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
            )
        )

    return render_template(
        "index.html", domains=domains, form=form, public_ip=public_ip
    )
