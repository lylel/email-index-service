from typing import List

from src.api.schemas import Email
from src.repository.email import EmailRepository
from src.services.utils import TextSearchOptimizer


class EmailService:
    @staticmethod
    def import_email(
        sender,
        recipient,
        subject,
        timestamp,
        message_content,
        search_optimizer=TextSearchOptimizer,
    ):
        if search_optimizer:
            message_content = search_optimizer(message_content).optimize()
        # Convert ORM to Pydantic
        # from_orm https://docs.pydantic.dev/latest/concepts/models/
        return EmailRepository.add(
            sender=sender,
            recipient=recipient,
            subject=subject,
            timestamp=timestamp,
            message_content=message_content,
        )

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
        return EmailRepository.search(
            keywords=keywords,
            sender=sender,
            recipient=recipient,
            to_or_from_address=to_or_from_address,
            after=after,
            before=before,
        )
