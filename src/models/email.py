from peewee import Model, CharField, BigIntegerField

from src.db import db


class Email(Model):
    sender_email = CharField()
    receiver_email = CharField()
    cc_receiver_emails = CharField()
    subject = CharField()
    timestamp = BigIntegerField()
    message_content = CharField()
    searchable_text = CharField()

    class Meta:
        database = db
