from peewee import Model, CharField, BigIntegerField

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
