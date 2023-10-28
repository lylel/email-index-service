from functools import reduce

from src.models.email import Email


class EmailRepository:
    # Rename to EmailPeeWeeRepo?
    @staticmethod
    def add(sender, recipient, subject, timestamp, message_content):
        return Email.create(
            sender=sender,
            recipient=recipient,
            subject=subject,
            timestamp=timestamp,
            message_content=message_content,
        )

    @staticmethod
    def search(
        keywords=None,
        sender=None,
        recipient=None,
        to_or_from_address=None,
        after=None,
        before=None,
    ):
        query = Email.select()

        if keywords:
            conditions = [Email.message_content.contains(word) for word in keywords]
            combined_condition = reduce(lambda x, y: x & y, conditions)
            query = query.where(combined_condition)

        if to_or_from_address:
            query = query.where(
                (Email.sender == to_or_from_address)
                | (Email.recipient == to_or_from_address)
            )
        else:
            if sender:
                query = query.where(Email.sender == sender)
            if recipient:
                query = query.where(Email.recipient == recipient)

        if after:
            query = query.where(Email.timestamp > after)
        if before:
            query = query.where(Email.timestamp < before)

        return [email for email in query]
