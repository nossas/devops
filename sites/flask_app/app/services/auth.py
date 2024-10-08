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
    # user_id is a token
    return User(user_id, session.get("first_name"))
