from typing import List

from src.models.email import Email
from src.repository.peewee_sqlite import Repository


class SearchEngine:
    def __init__(self, repository=None):
        self._repository = repository

    @property
    def repository(self):
        return self._repository or Repository

    def search(
        self,
        keywords: List = None,
        addressed_from: str = None,
        recipient: str = None,
        sender_or_recipient: str = None,
        after: int = None,
        before: int = None,
    ) -> list[Email]:
        return self.repository().find_all(
            keywords=keywords,
            sender=addressed_from,
            recipient=recipient,
            sender_or_recipient=sender_or_recipient,
            after=after,
            before=before,
        )
