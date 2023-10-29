from peewee import Model, CharField, BigIntegerField, ForeignKeyField

from src.db import db


class Email(Model):
    addressed_from = CharField()
    addressed_to = CharField()
    cc_recipients = CharField()
    actual_recipient = CharField()
    subject = CharField()
    timestamp = BigIntegerField()
    message_content = CharField()
    searchable_text = CharField()

    class Meta:
        database = db



class Email(Model):
    sender = CharField()
    recipient = CharField()
    message_content = CharField()


class EmailCarbonCopy(Model):
    email_id = ForeignKeyField(Email, backref='carbon_copies')
    cc_recipient = CharField()
