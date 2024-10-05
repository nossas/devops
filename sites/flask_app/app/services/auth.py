from flask import session
from flask_login import UserMixin, login_user
import requests

from ..extensions import login_manager


class User(UserMixin):

    def __init__(self, token, first_name):
        self.id = token
        self.first_name = first_name


@login_manager.user_loader
def load_user(user_id):
    # session.get("token")
    return User(user_id, session.get("first_name"))


def verify_user(username, password):
    url = "https://api-graphql.staging.bonde.org/v1/graphql"

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
        url, json={"query": query, "variables": variables}, headers=headers
    )
    if response.status_code == 200:
        response_json = response.json()
        if "data" in response_json:
            return (
                response_json["data"]["authenticate"]["first_name"],
                response_json["data"]["authenticate"]["token"],
            )
    return None, None
