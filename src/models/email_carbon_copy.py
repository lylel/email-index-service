from peewee import Model, CharField, ManyToManyField

from src.db import db
from src.models.email import Email


class EmailCarbonCopy(Model):
    # TODO: ADD INDICES
    email = ManyToManyField(Email, backref="carbon_copies")
    receiver = CharField()

    class Meta:
        database = db
