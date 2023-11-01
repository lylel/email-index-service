import pytest
from starlette.testclient import TestClient

from src.main import app
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy
from tests.conftest import test_db

client = TestClient(app)


@pytest.mark.usefixtures("test_db")
class TestImportEmail:
    @property
    def request_json(self):
        return {
            "sender_email": "e2e.test@continua.ai",
            "receiver_email": "candidate@continua.ai",
            "cc_receiver_emails": ["hiring@continua.ai"],
            "subject": "Welcome to Continua",
            "timestamp": 1690569041,
            "message_content": "Welcome! On your first day…",
        }

    def test_import_email__correct_response(self):
        response = client.post("/v1/emails", json=self.request_json)
        response_json = response.json()

        assert response.status_code == 201
        assert response_json["sender_email"] == self.request_json["sender_email"]
        assert response_json["receiver_email"] == self.request_json["receiver_email"]
        assert (
            response_json["cc_receiver_emails"]
            == self.request_json["cc_receiver_emails"]
        )
        assert response_json["subject"] == self.request_json["subject"]
        assert response_json["timestamp"] == self.request_json["timestamp"]
        assert response_json["message_content"] == self.request_json["message_content"]

    def test_import_email__email_inserted(self):
        assert Email.select().count() == 0

        response = client.post("/v1/emails", json=self.request_json)
        assert response.status_code == 201

        emails = Email.select()
        assert len(emails) == 1

        email = emails[0]
        assert email.sender_email == self.request_json["sender_email"]
        assert email.receiver_email == self.request_json["receiver_email"]
        assert (
            email.cc_receiver_emails.split(", ")
            == self.request_json["cc_receiver_emails"]
        )
        assert email.subject == self.request_json["subject"]
        assert email.timestamp == self.request_json["timestamp"]
        assert email.message_content == self.request_json["message_content"]

    def test_import_email__carbon_copy_imported(self):
        assert EmailCarbonCopy.select().count() == 0

        response = client.post("/v1/emails", json=self.request_json)
        assert response.status_code == 201

        carbon_copies = EmailCarbonCopy.select()
        assert len(carbon_copies) == len(self.request_json["cc_receiver_emails"])

        carbon_copy = carbon_copies[0]
        assert carbon_copy.receiver_email == self.request_json["cc_receiver_emails"][0]

        email = carbon_copy.email
        assert email.sender_email == self.request_json["sender_email"]
        assert email.receiver_email == self.request_json["receiver_email"]
        assert (
            email.cc_receiver_emails.split(", ")
            == self.request_json["cc_receiver_emails"]
        )
        assert email.subject == self.request_json["subject"]
        assert email.timestamp == self.request_json["timestamp"]
        assert email.message_content == self.request_json["message_content"]

    @pytest.mark.parametrize(
        "missing_field", ["sender_email", "receiver_email", "timestamp"]
    )
    def test_import_email__missing_field__returns_error(self, missing_field):
        request_json = self.request_json
        request_json.pop(missing_field)

        response = client.post("/v1/emails", json=request_json)
        response_json = response.json()

        assert response.status_code == 422
        assert response.is_error

        assert response_json["detail"][0]["type"] == "missing"
        assert response_json["detail"][0]["loc"] == ["body", missing_field]
        assert response_json["detail"][0]["msg"] == "Field required"
