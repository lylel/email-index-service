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
        sender_email="people.ops@continua.ai",
        receiver_email="candidate@continua.ai",
        cc_receiver_emails="hiring@continua.ai",
        subject="Hello!     World@@@@@@",
        timestamp=1690569041,
        message_content="#(%*&(!&%#!Some |||| Random -----    Words",
        searchable_text="Hello World Some Random Words",
    ):
        email = Email.create(
            sender_email=sender_email,
            receiver_email=receiver_email,
            cc_receiver_emails=cc_receiver_emails,
            subject=subject,
            timestamp=timestamp,
            message_content=message_content,
            searchable_text=searchable_text,
        )
        return email

    return _an_email
