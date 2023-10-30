from functools import reduce

from peewee import fn

from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy


def contains(keywords, q):
    if keywords:
        return q.where(Email.searchable_text.contains(keywords))
    return q


def sender_or_recipient_is(address, q):
    if address:
        return q.where(
            (Email.sender == address)
            | (Email.recipient == address)
            | (EmailCarbonCopy.recipient == address)
        )
    return q


def sender_is(address, q):
    if address:
        return q.where(Email.sender == address)
    return q


def recipient_is(address, q):
    if address:
        return q.where(
            (Email.recipient == address) | (EmailCarbonCopy.recipient == address)
        )
    return q


def is_after(timestamp, q):
    if timestamp:
        return q.where(Email.timestamp > timestamp)
    return q


def is_before(timestamp, q):
    if timestamp:
        return q.where(Email.timestamp < timestamp)
    return q
