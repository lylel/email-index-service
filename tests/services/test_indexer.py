import pytest

from src.api.schemas import EmailRequest
from src.services.indexer import Indexer
from tests.conftest import test_db


@pytest.mark.usefixtures("test_db")
class TestIndexer:
    @property
    def email_request(self):
        return EmailRequest(
            sender_email="people.ops@continua.ai",
            receiver_email="candidate@continua.ai",
            cc_receiver_emails=["hiring@continua.ai"],
            subject="Welcome to Continua",
            timestamp=1690569041,
            message_content="Welcome! On your first day…",
        )

    def test_ingest(self):
        email = Indexer().ingest(email=self.email_request)

        assert email.sender_email == self.email_request.sender_email
        assert email.receiver_email == self.email_request.receiver_email
        assert email.cc_receiver_emails == ", ".join(
            self.email_request.cc_receiver_emails
        )
        assert email.subject == self.email_request.subject
        assert email.timestamp == self.email_request.timestamp
        assert email.message_content == self.email_request.message_content
        assert (
            email.searchable_text
            == "Welcome [profanity] Continua Welcome On your first day"
        )
