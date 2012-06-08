from django.db.models import CharField, BooleanField
from django.db.models.base import Model


class SomeModel(Model):
    name = CharField(max_length=200)
    email = CharField(max_length=200)
    dangerous_field_1 = BooleanField(default=False)
    dangerous_field_2 = BooleanField(default=False)
