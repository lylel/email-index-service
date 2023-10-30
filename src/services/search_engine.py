from typing import List

from src.repository.peewee_sqlite import Repository


class SearchEngine:
    def __init__(self, repository=None):
        self._repository = repository

    @staticmethod
    def search(
        keywords: List = None,
        addressed_from: str = None,
        recipient: str = None,
        sender_or_recipient: str = None,
        after: int = None,
        before: int = None,
    ):
        if not (
            keywords
            or addressed_from
            or recipient
            or sender_or_recipient
            or after
            or before
        ):
            return []  # What?
        return Repository.find_all(
            keywords=keywords,
            sender=addressed_from,
            recipient=recipient,
            sender_or_recipient=sender_or_recipient,
            after=after,
            before=before,
        )
