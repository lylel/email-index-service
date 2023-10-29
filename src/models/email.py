from peewee import Model, CharField, BigIntegerField

from src.db import db


class Email(Model):
    sender = CharField()
    recipient = CharField()
    cc_recipients = CharField()
    subject = CharField()
    timestamp = BigIntegerField()
    message_content = CharField()
    searchable_text = CharField()

    class Meta:
        database = db
