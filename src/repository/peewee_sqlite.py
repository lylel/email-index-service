from src.db import db
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy
from src.repository.peewee_sqlite_queryset import (
    has_keywords,
    recipient_or_sender_is,
    is_sender,
    is_after,
    is_before,
    is_recipient,
)
from src.services.schemas import EmailArgs


class Repository:
    def add_email_with_carbon_copies(self, email_args: EmailArgs):
        with db.atomic():
            new_email = self._add_email(email_args)
            self._add_carbon_copies(new_email, email_args)

        return new_email

    @staticmethod
    def find_all(
        keywords=None,
        sender=None,
        recipient=None,
        sender_or_recipient=None,
        after=None,
        before=None,
    ):
        q = Email.select().join(EmailCarbonCopy)
        q = has_keywords(keywords, q)
        q = is_sender(sender, q)
        q = is_recipient(recipient, q)
        q = recipient_or_sender_is(sender_or_recipient, q)
        q = is_after(after, q)
        q = is_before(before, q)

        return q.execute()

    def _add_email(self, email_args: EmailArgs):
        return Email.create(**email_args.model_dump())

    def _add_carbon_copies(self, new_email, email_args):
        with db.atomic():
            carbon_copy_data = [
                {"email": new_email, "recipient": recipient}
                for recipient in email_args.cc_recipients
            ]
            EmailCarbonCopy.insert_many(carbon_copy_data).execute()
