from typing import List

from src.repository.email import EmailRepository
from src.services.utils import TextSearchOptimizer


class EmailService:
    @staticmethod
    def import_email(
        sender,
        recipient,
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
            sender=sender,
            recipient=recipient,
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
        sender: str = None,
        recipient: str = None,
        to_or_from_address: str = None,
        after: int = None,
        before: int = None,
    ):
        if not (
            keywords or sender or recipient or to_or_from_address or after or before
        ):
            return  # What?
        return EmailRepository.query(
            keywords=keywords,
            sender=sender,
            recipient=recipient,
            to_or_from_address=to_or_from_address,
            after=after,
            before=before,
        )
