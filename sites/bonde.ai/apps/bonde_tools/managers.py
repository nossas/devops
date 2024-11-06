from django.db import models


class BondeToolsManager(models.Manager):

    def __init__(self, lookup_field=None):
        self.lookup_field = lookup_field
        super().__init__()

    def for_user(self, user):
        if user.is_superuser:
            return self.all()
        
        return self.filter(**{self.lookup_field: user})