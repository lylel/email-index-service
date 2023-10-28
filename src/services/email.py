from typing import List

from src.repository.email import EmailRepository
from src.services.utils import TextSearchOptimizer


class EmailService:
    @staticmethod
    def import_email(
        addressed_from,
        addressed_to,
        cc_recipients,
        subject,
        timestamp,
        message_content,
        search_optimizer=TextSearchOptimizer,
    ):
        # This needs to be abstracted
        searchable_text = subject + " " + message_content
        if search_optimizer:
            searchable_text = search_optimizer(searchable_text).optimize()

        email = EmailRepository().create_with_carbon_copies(
            addressed_from=addressed_from,
            addressed_to=addressed_to,
            cc_recipients=cc_recipients,
            subject=subject,
            timestamp=timestamp,
            message_content=message_content,
            searchable_text=searchable_text,
        )
        # Convert ORM to Pydantic
        # from_orm https://docs.pydantic.dev/latest/concepts/models/
        return email

    @staticmethod
    def search(
        keywords: List = None,
        addressed_from: str = None,
        recipient: str = None,
        to_or_from_address: str = None,
        after: int = None,
        before: int = None,
    ):
        if not (
            keywords
            or addressed_from
            or recipient
            or to_or_from_address
            or after
            or before
        ):
            return []  # What?
        return EmailRepository.query(
            keywords=keywords,
            addressed_from=addressed_from,
            actual_recipient=recipient,
            to_or_from_address=to_or_from_address,
            after=after,
            before=before,
        )
