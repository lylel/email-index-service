from typing import List

from src.api.schemas import Email
from src.services.schemas import EmailArgs
from src.services.utils import TextSearchOptimizer


class PreProcessor:
    def __init__(self, email: Email, search_optimizer=None):
        self._email = email
        self._search_optimizer = search_optimizer
        self._searchable_text = None

    @property
    def email(self):
        return self._email

    @property
    def search_optimizer(self):
        return self._search_optimizer or TextSearchOptimizer

    @property
    def searchable_text(self):
        return self.email.subject + " " + self.email.message_content

    @searchable_text.setter
    def searchable_text(self, value):
        self._searchable_text = value

    def prepare(self):
        self.searchable_text = self.search_optimizer(self.searchable_text).optimize()
        return self.map()

    def map(self) -> EmailArgs:
        return EmailArgs(
            sender=self.email.sender_email,
            recipient=self.email.receiver_email,
            cc_recipients=self.email.cc_receiver_emails,
            # actual_recipient=self.email.receiver_email,
            subject=self.email.subject,
            timestamp=self.email.timestamp,
            message_content=self.email.message_content,
            searchable_text=self.searchable_text,
        )
