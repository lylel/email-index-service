from peewee import Model, ForeignKeyField, CharField

from src.db import db
from src.models.email import Email


class EmailCarbonCopy(Model):
    email = ForeignKeyField(Email, backref="carbon_copies")
    receiver_email = CharField()

    class Meta:
        database = db
