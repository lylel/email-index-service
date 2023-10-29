from functools import reduce

from peewee import fn

from src.db import db
from src.models.email import Email
from src.services.schemas import EmailArgs


class SQLiteRepository:
    @staticmethod
    def add(
        addressed_from,
        addressed_to,
        cc_recipients,
        subject,
        timestamp,
        message_content,
        searchable_text,
    ):
        # Decide between single object parameter and large list of args
        return Email.create(
            addressed_from=addressed_from,
            addressed_to=addressed_to,
            cc_recipients=", ".join(cc_recipients),
            actual_recipient=addressed_to,
            subject=subject,
            timestamp=timestamp,
            message_content=message_content,
            searchable_text=searchable_text,
        )

    def create_with_carbon_copies(self, email_args: EmailArgs):
        with db.atomic():
            args_dict = email_args.model_dump()
            self.add(**args_dict)

            carbon_copies = []
            for cc_recipient in email_args.cc_recipients:
                cc_dict = args_dict.copy()
                cc_dict["actual_recipient"] = cc_recipient
                carbon_copies.append(cc_dict)
            Email.insert_many(carbon_copies).execute()
        return

    @staticmethod
    def query(
        keywords=None,
        addressed_from=None,
        actual_recipient=None,
        to_or_from_address=None,
        after=None,
        before=None,
    ):
        q = Email.select()

        if keywords:
            conditions = [
                fn.Lower(Email.searchable_text.contains(word.lower()))
                for word in keywords
            ]
            combined_condition = reduce(lambda x, y: x & y, conditions)
            q = q.where(combined_condition)

        if to_or_from_address:
            q = q.where(
                (Email.addressed_from == to_or_from_address)
                | (Email.recipient == to_or_from_address)
            )
        else:
            if addressed_from:
                q = q.where(Email.addressed_from == addressed_from)
            if actual_recipient:
                q = q.where(Email.recipient == actual_recipient)

        if after:
            q = q.where(Email.timestamp > after)
        if before:
            q = q.where(Email.timestamp < before)

        return [email for email in q]

    def query_constructor(self):
        pass