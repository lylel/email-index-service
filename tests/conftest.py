import pytest

from src.db import db
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy


@pytest.fixture(scope="function")
def test_db():
    db.init(":memory:")
    db.connect()
    db.create_tables([Email, EmailCarbonCopy])

    yield

    db.drop_tables([Email, EmailCarbonCopy])
    db.close()


@pytest.fixture(scope="function")
def an_email():
    def _an_email(
        sender="people.ops@continua.ai",
        recipient="candidate@continua.ai",
        cc_recipients="hiring@continua.ai",
        subject="Welcome to Continua",
        timestamp=1690569041,
        message_content="Welcome! On your first day…",
        searchable_text="Welcome to Continua Welcome On your first day",
    ):
        email = Email.create(
            sender=sender,
            recipient=recipient,
            cc_recipients=cc_recipients,
            subject=subject,
            timestamp=timestamp,
            message_content=message_content,
            searchable_text=searchable_text,
        )
        return email

    return _an_email
