from functools import reduce

from peewee import fn

from src.db import db
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy
from src.services.schemas import EmailArgs


class Repository:
    @staticmethod
    def add(email_args: EmailArgs):
        # Decide between single object parameter and large list of args
        return Email.create(**email_args.model_dump())

    def create_with_carbon_copies(self, email_args: EmailArgs):
        with db.atomic():
            new_email = self.add(email_args)

            with db.atomic():
                carbon_copy_data = [
                    {"email": new_email, "recipient": recipient}
                    for recipient in email_args.cc_recipients
                ]
                EmailCarbonCopy.insert_many(carbon_copy_data).execute()
        return

    @staticmethod
    # Rename to repository convention, get? Find synonym for multi get
    def query(
        keywords=None,
        sender=None,
        recipient=None,
        to_or_from_address=None,
        after=None,
        before=None,
    ):
        print(333333333)
        q = Email.select().join(EmailCarbonCopy)

        if keywords:
            conditions = [
                fn.Lower(Email.searchable_text.contains(word.lower()))
                for word in keywords
            ]
            combined_condition = reduce(lambda x, y: x & y, conditions)
            q = q.where(combined_condition)

        if to_or_from_address:
            q = q.where(
                (Email.sender == to_or_from_address)
                | (Email.recipient == to_or_from_address)
                | (EmailCarbonCopy.recipient == to_or_from_address)
            )
        else:
            if sender:
                q = q.where(Email.sender == sender)
            if recipient:
                q = q.where(
                    (Email.recipient == recipient)
                    | (EmailCarbonCopy.recipient == recipient)
                )

        if after:
            q = q.where(Email.timestamp > after)
        if before:
            q = q.where(Email.timestamp < before)

        results = [email for email in q]
        print(results)
        return results

    def query_constructor(self):
        pass
