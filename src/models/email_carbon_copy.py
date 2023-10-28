from peewee import Model, ForeignKeyField, CharField

from src.db import db
from src.models.email import Email


class EmailCarbonCopy(Model):
    # TODO: ADD INDICES
    email = ForeignKeyField(Email)
    recipient = CharField()

    class Meta:
        database = db

    # Unique constraint between email + recipient
