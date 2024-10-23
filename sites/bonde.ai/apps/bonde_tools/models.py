from django.db import models
from django.contrib.auth.models import User

from .managers import BondeToolsManager


class Community(models.Model):
    name = models.CharField(max_length=100)
    external_id = models.PositiveIntegerField(null=True, blank=True)
    users = models.ManyToManyField(User, blank=True)

    objects = BondeToolsManager("users")

    def __str__(self):
        return self.name