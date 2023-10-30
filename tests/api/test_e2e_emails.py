import pytest
from starlette.testclient import TestClient

from main import app
from src.models.email import Email
from tests.conftest import test_db


client = TestClient(app)


@pytest.mark.usefixtures("test_db")
class TestEmailsAPI:
    def test_import_email(self):
        initial_email_count = Email.select().count()
        response = client.post(
            "/v1/emails",
            json={
                "sender_email": "e2e.test@continua.ai",
                "receiver_email": "candidate@continua.ai",
                "cc_receiver_emails": ["hiring@continua.ai"],
                "subject": "Welcome to Continua",
                "timestamp": 1690569041,
                "message_content": "Welcome.  @! On  apple     your  ...     first day…",
            },
        )
        assert response.status_code == 200
        assert Email.select().count() == initial_email_count + 1
