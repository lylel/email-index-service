from functools import reduce

from peewee import fn

from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy


def contains(keywords, q):
    if keywords:
        conditions = [
            fn.Lower(Email.searchable_text.contains(word.lower())) for word in keywords
        ]
        combined_condition = reduce(lambda x, y: x & y, conditions)
        return q.where(combined_condition)
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
