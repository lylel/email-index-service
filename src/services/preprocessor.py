from src.api.schemas import EmailRequest
from src.services.schemas import EmailArgs
from src.services.text_search_optimizer import TextSearchOptimizer


class PreProcessor:
    def __init__(self, search_optimizer=None):
        self._search_optimizer = search_optimizer

    @property
    def search_optimizer(self):
        return self._search_optimizer or TextSearchOptimizer

    def prepare(self, email: EmailRequest) -> EmailArgs:
        searchable_text = self.generate_searchable_text(email)
        return self.map(email, searchable_text)

    def generate_searchable_text(self, email: EmailRequest):
        searchable_text = ""
        if email.subject:
            searchable_text += email.subject
        if email.message_content:
            if searchable_text:
                searchable_text += " "
            searchable_text += email.message_content

        return self.search_optimizer(text=searchable_text).optimize()

    def map(self, email, searchable_text) -> EmailArgs:
        return EmailArgs(
            sender=email.sender_email,
            recipient=email.receiver_email,
            cc_recipients=email.cc_receiver_emails,
            subject=email.subject,
            timestamp=email.timestamp,
            message_content=email.message_content,
            searchable_text=searchable_text,
        )
