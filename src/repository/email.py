from functools import reduce

from peewee import fn

from src.db import db
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy


class EmailRepository:
    # Rename to EmailPeeWeeRepo?
    @staticmethod
    def create(sender, recipient, subject, timestamp, message_content, searchable_text):
        return Email.create(
            sender=sender,
            recipient=recipient,
            subject=subject,
            timestamp=timestamp,
            message_content=message_content,
            searchable_text=searchable_text,
        )

    @staticmethod
    def create_carbon_copies(original, recipients):
        with db.atomic():
            carbon_copy_data = [
                {"email": original, "recipient": recipient} for recipient in recipients
            ]
            EmailCarbonCopy.insert_many(carbon_copy_data).execute()

    def create_with_carbon_copies(
        self,
        sender,
        recipient,
        cc_recipients,
        subject,
        timestamp,
        message_content,
        searchable_text,
    ):
        with db.atomic():
            email = self.create(
                sender, recipient, subject, timestamp, message_content, searchable_text
            )
            self.create_carbon_copies(original=email, recipients=cc_recipients)
        return email

    @staticmethod
    def query(
        keywords=None,
        sender=None,
        recipient=None,
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
                (Email.sender == to_or_from_address)
                | (Email.recipient == to_or_from_address)
            )
        else:
            if sender:
                q = q.where(Email.sender == sender)
            if recipient:
                q = q.where(Email.recipient == recipient)

        if after:
            q = q.where(Email.timestamp > after)
        if before:
            q = q.where(Email.timestamp < before)

        return [email for email in q]
