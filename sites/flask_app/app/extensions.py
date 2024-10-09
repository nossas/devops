from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import requests


class BondeAPIExtension:
    def __init__(self, app=None):
        self.api_url = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.api_url = app.config.get("BONDE_API_URL")
        app.bonde_api = self  # Disponibiliza a extensão globalmente
    
    def raise_or_token(self):
        token = session.get("token")
        if not token:
            raise Exception("User is not authenticated")
        return token

    def get_headers(self):
        token = self.raise_or_token()
        return {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    def get_cookies(self):
        """BONDE usa autenticação por Cookie de Sessão, é importante conferir se
        seu o domínio dessa aplicação está no CORS da API"""
        token = self.raise_or_token()
        return {"session": token}

    def authenticate(self, username, password):
        query = """
        mutation login($email: String!, $password: String!) {
            authenticate(email: $email, password: $password) {
                first_name
                token
            }
        }
        """
        variables = {"email": username, "password": password}
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self.api_url, json={"query": query, "variables": variables}, headers=headers
        )
        if response.status_code == 200:
            response_json = response.json()
            if "data" in response_json:
                token = response_json["data"]["authenticate"]["token"]
                first_name = response_json["data"]["authenticate"]["first_name"]

                # Armazena na sessão
                session["token"] = token
                session["first_name"] = first_name

                return token, first_name

        return None, None

    def get_communities(self):
        headers = self.get_headers()
        cookies = self.get_cookies()
        query = """
        query communities {
            communities {
                id
                name
            }
        }
        """
        response = requests.post(
            self.api_url, json={"query": query}, cookies=cookies, headers=headers
        )

        if response.status_code == 200:
            response_json = response.json()
            if "data" in response_json:
                communities = response_json["data"]["communities"]
                return list(map(lambda x: (x.get("id"), x.get("name")), communities))

        return []

    def get_community_by_id(self, id):
        headers = self.get_headers()
        cookies = self.get_cookies()
        query = """
        query {
            communities_by_pk(id: 10) {
                id
                name
            }
        }
        """
        response = requests.post(
            self.api_url, json={"query": query}, cookies=cookies, headers=headers
        )

        if response.status_code == 200:
            response_json = response.json()
            if "data" in response_json:
                community = response_json["data"]["communities_by_pk"]
                return community

        return None


db = SQLAlchemy()

login_manager = LoginManager()

bonde_api = BondeAPIExtension()
