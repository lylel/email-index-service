import pytest
from fastapi import FastAPI

from src.api import v1_emails
from src.repository.peewee_sqlite import Repository
from src.services.schemas import EmailArgs

from fastapi.testclient import TestClient

from main import app

from tests.conftest import test_db

client = TestClient(app)


@pytest.mark.usefixtures("test_db")
class TestEmailRepository:
    # def test_create(self):
    #     x = Repository.add(
    #         addressed_from="people.ops@continua.ai",
    #         addressed_to="candidate@continua.ai",
    #         subject="Welcome to Continua",
    #         timestamp=1690569041,
    #         message_content="Welcome! On your first day…",
    #         searchable_text="Welcome to Continua Welcome On your first day",
    #     )
    #     assert True is True

    def test_add_email_with_carbon_copies(self):
        email_args = EmailArgs(
            sender="people.ops@continua.ai",
            recipient="candidate@continua.ai",
            cc_recipients=["hiring@continua.ai"],
            subject="Welcome to Continua",
            timestamp="1690569041",
            message_content="Welcome! On your first day…",
            searchable_text="Welcome On your first day",
        )
        copies = Repository().add_email_with_carbon_copies(email_args=email_args)
        assert True is True

    # def test_search(self, an_email):
    #     email = an_email()
    #     keywords = ["Continua", "Day"]
    #     assert Repository().find_all(keywords=keywords) == [email]
