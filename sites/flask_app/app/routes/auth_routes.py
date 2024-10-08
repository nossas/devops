from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user

from ..services.auth import User
from ..extensions import bonde_api


auth_routes = Blueprint("auth", __name__, url_prefix="/auth")


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Autentica o usuário via API GraphQL e armazena na sessão
        token, first_name = bonde_api.authenticate(username, password)
        if first_name and token:            
            user = User(token, first_name)
            login_user(user)

            return redirect(url_for("main.index"))
        else:
            return "Login falhou!"
    
    return render_template("login.html")


@auth_routes.route("/logout")
def logout():
    logout_user()
    session.pop("token", None)
    session.pop("first_name", None)
    return redirect(url_for('auth.login'))