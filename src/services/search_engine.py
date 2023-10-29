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
        to_or_from_address: str = None,
        after: int = None,
        before: int = None,
    ):
        print(222222222)
        if not (
            keywords
            or addressed_from
            or recipient
            or to_or_from_address
            or after
            or before
        ):
            return []  # What?
        return Repository.query(
            keywords=keywords,
            sender=addressed_from,
            recipient=recipient,
            to_or_from_address=to_or_from_address,
            after=after,
            before=before,
        )
