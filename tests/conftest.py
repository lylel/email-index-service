import pytest

from src.db import db
from src.models.email import Email


@pytest.fixture(scope="function")
def test_db():
    db.init(":memory:")
    db.connect()
    db.create_tables([Email])
    yield
    db.drop_tables([Email])
    db.close()


@pytest.fixture(scope="function")
def an_email():
    def _an_email(
        addressed_from="people.ops@continua.ai",
        addressed_to="candidate@continua.ai",
        actual_recipient="candidate@continua.ai",
        cc_recipients="hiring@continua.ai",
        subject="Welcome to Continua",
        timestamp=1690569041,
        message_content="Welcome! On your first day…",
        searchable_text="Welcome to Continua Welcome On your first day",
    ):
        email = Email.create(
            addressed_from=addressed_from,
            addressed_to=addressed_to,
            actual_recipient=actual_recipient,
            cc_recipients=cc_recipients,
            subject=subject,
            timestamp=timestamp,
            message_content=message_content,
            searchable_text=searchable_text,
        )
        return email

    return _an_email
