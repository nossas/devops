from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User, Group
import requests


class ExternalAPIAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        """Authenticate with user credentials in Bonde GraphQL API"""
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
            "https://api-graphql.staging.bonde.org/v1/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if response.status_code == 200:
            response_json = response.json()
            if "data" in response_json and response_json.get("data", None):
                token = response_json["data"]["authenticate"]["token"]
                first_name = response_json["data"]["authenticate"]["first_name"]

                if token:
                    user, _ = User.objects.get_or_create(
                        username=username,
                        email=username,
                        first_name=first_name,
                        is_staff=True
                    )
                    user.groups.set(Group.objects.filter(name="Usuário Padrão"))
                    user.save()

                    # Armazena na sessão
                    request.session["auth_token"] = token

                    return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
