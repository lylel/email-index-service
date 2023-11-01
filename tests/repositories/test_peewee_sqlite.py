import pytest

from src.models.email_carbon_copy import EmailCarbonCopy
from src.repositories.peewee_sqlite import Repository
from src.services.schemas import EmailArgs

from fastapi.testclient import TestClient

from src.main import app
from tests.conftest import test_db

client = TestClient(app)


@pytest.mark.usefixtures("test_db")
class TestRepository:
    @property
    def email_args(self):
        return EmailArgs(
            sender_email="people.ops@continua.ai",
            receiver_email="candidate@continua.ai",
            cc_receiver_emails=["hiring@continua.ai"],
            subject="Hello World",
            timestamp="1690569041",
            message_content="Welcome to Continua! On your first day…",
            searchable_text="Hello World Welcome to Continua On your first day",
        )

    def test_add_email_with_carbon_copies__successful_email_insert(self):
        email = Repository().add_email_with_carbon_copies(email_args=self.email_args)
        assert email.sender_email == self.email_args.sender_email
        assert email.receiver_email == self.email_args.receiver_email
        assert (
            email.cc_receiver_emails.split(", ") == self.email_args.cc_receiver_emails
        )
        assert email.subject == self.email_args.subject
        assert email.timestamp == self.email_args.timestamp
        assert email.message_content == self.email_args.message_content
        assert email.searchable_text == self.email_args.searchable_text

    def test_add_email_with_carbon_copies__successful_carbon_copy_insert(self):
        assert EmailCarbonCopy.select().count() == 0

        Repository().add_email_with_carbon_copies(email_args=self.email_args)

        assert EmailCarbonCopy.select().count() == 1

        carbon_copy = EmailCarbonCopy.select()[0]
        assert carbon_copy.receiver_email == self.email_args.cc_receiver_emails[0]

        assert carbon_copy.email.sender_email == self.email_args.sender_email
        assert carbon_copy.email.receiver_email == self.email_args.receiver_email
        assert (
            carbon_copy.email.cc_receiver_emails.split(", ")
            == self.email_args.cc_receiver_emails
        )
        assert carbon_copy.email.subject == self.email_args.subject
        assert carbon_copy.email.timestamp == self.email_args.timestamp
        assert carbon_copy.email.message_content == self.email_args.message_content
        assert carbon_copy.email.searchable_text == self.email_args.searchable_text
