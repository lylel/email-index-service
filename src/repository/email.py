from functools import reduce

from peewee import fn

from src.db import db
from src.models.email import Email


class EmailRepository:
    # Rename to EmailPeeWeeRepo?
    @staticmethod
    def create(
        addressed_from,
        addressed_to,
        cc_recipients,
        subject,
        timestamp,
        message_content,
        searchable_text,
    ):
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

    def create_with_carbon_copies(
        self,
        addressed_from,
        addressed_to,
        cc_recipients,
        subject,
        timestamp,
        message_content,
        searchable_text,
    ):
        with db.atomic():
            self.create(
                addressed_from,
                addressed_to,
                cc_recipients,
                subject,
                timestamp,
                message_content,
                searchable_text,
            )
            carbon_copies = [
                {
                    "addressed_from": addressed_from,
                    "addressed_to": addressed_to,
                    "cc_recipients": ", ".join(cc_recipients),
                    "actual_recipient": cc_recipient,
                    "subject": subject,
                    "timestamp": timestamp,
                    "message_content": message_content,
                    "searchable_text": searchable_text,
                }
                for cc_recipient in cc_recipients
            ]
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
