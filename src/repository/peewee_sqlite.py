from src.db import db
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy
from src.repository.query_filters import (
    contains,
    sender_or_recipient_is,
    sender_is,
    is_after,
    is_before,
    recipient_is,
)
from src.repository.schemas import SearchRequest
from src.services.schemas import EmailArgs


class Repository:
    def add_email_with_carbon_copies(self, email_args: EmailArgs) -> Email:
        with db.atomic():
            new_email = self._add_email(email_args)
            self._add_carbon_copies(new_email, email_args)
        return new_email

    def find_all(self, search_request: SearchRequest) -> list[Email]:
        q = Email.select().left_outer_join(EmailCarbonCopy)
        q = contains(search_request.keywords, q)
        q = sender_is(search_request.sender, q)
        q = recipient_is(search_request.recipient, q)
        q = sender_or_recipient_is(search_request.sender_or_recipient, q)
        q = is_after(search_request.after, q)
        q = is_before(search_request.before, q)
        q = q.distinct()

        return [email for email in q]

    def _add_email(self, email_args: EmailArgs) -> Email:
        return Email.create(**email_args.model_dump())

    def _add_carbon_copies(self, new_email, email_args):
        with db.atomic():
            carbon_copy_data = [
                {"email": new_email, "recipient": recipient}
                for recipient in email_args.cc_recipients
            ]
            EmailCarbonCopy.insert_many(carbon_copy_data).execute()
