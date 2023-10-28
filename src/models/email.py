from peewee import Model, CharField, BigIntegerField

from src.db import db


class Email(Model):
    # TODO: ADD INDICES
    sender = CharField()
    recipient = CharField()
    subject = CharField()
    timestamp = BigIntegerField()
    message_content = CharField()

    class Meta:
        database = db


# class CarbonCopy(Email):
#
#     class Meta:
#         database = db
