from typing import List

from src.repository.email import EmailSQLiteRepository


class SearchEngine:
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
        return EmailSQLiteRepository.query(
            keywords=keywords,
            addressed_from=addressed_from,
            actual_recipient=recipient,
            to_or_from_address=to_or_from_address,
            after=after,
            before=before,
        )
