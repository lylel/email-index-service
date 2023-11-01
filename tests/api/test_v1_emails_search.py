import pytest
from starlette.testclient import TestClient

from src.main import app
from src.models.email import Email
from tests.conftest import test_db, an_email

client = TestClient(app)


@pytest.mark.usefixtures("test_db")
class TestSearch:
    @property
    def request_json(self):
        return {
            "keywords": "Hello World",
            "sender_email": "e2e.test@continua.ai",
            "receiver_email": "candidate@continua.ai",
            "sender_or_recipient": ["hiring@continua.ai"],
            "after": 1690569033,
            "before": 1690569041,
            "message_content": "Welcome! On your first day…",
        }

    field_to_search = ["sender_email", "receiver_email"]

    @pytest.mark.parametrize("search_field", field_to_search)
    def test_search__addresses__correct_response(self, search_field, an_email):
        email = an_email()
        unmatched_email = an_email()
        setattr(unmatched_email, search_field, "invalid")
        unmatched_email.save()

        assert Email.select().count() == 2

        payload = {search_field: getattr(email, search_field)}
        response = client.get("/v1/emails", params=payload)
        response_json = response.json()

        assert response.status_code == 200
        assert len(response_json) == 1

        assert response_json[0]["sender_email"] == email.sender_email
        assert response_json[0]["receiver_email"] == email.receiver_email
        assert response_json[0]["cc_receiver_emails"] == email.cc_receiver_emails.split(
            ", "
        )
        assert response_json[0]["subject"] == email.subject
        assert response_json[0]["timestamp"] == email.timestamp
        assert response_json[0]["message_content"] == email.message_content

    field_to_search = ["sender_email", "receiver_email"]

    @pytest.mark.parametrize("search_field", field_to_search)
    def test_search__sender_or_recipient__correct_response(
        self, search_field, an_email
    ):
        sender_or_recipient_address = "hello@yahoo.com"
        email = an_email()
        setattr(email, search_field, sender_or_recipient_address)
        email.save()
        unmatched_email = an_email()

        assert Email.select().count() == 2

        payload = {"sender_or_recipient": sender_or_recipient_address}
        response = client.get("/v1/emails", params=payload)
        response_json = response.json()

        assert response.status_code == 200
        assert len(response_json) == 1

        assert response_json[0]["sender_email"] == email.sender_email
        assert response_json[0]["receiver_email"] == email.receiver_email
        assert response_json[0]["cc_receiver_emails"] == email.cc_receiver_emails.split(
            ", "
        )
        assert response_json[0]["subject"] == email.subject
        assert response_json[0]["timestamp"] == email.timestamp
        assert response_json[0]["message_content"] == email.message_content

    field_to_keyword_search = ["hello world", "body_content"]

    @pytest.mark.parametrize("search_field", field_to_keyword_search)
    def test_search__keyword_search__correct_response(self, search_field):
        request_json = {
            "sender_email": "e2e.test@continua.ai",
            "receiver_email": "candidate@continua.ai",
            "cc_receiver_emails": ["hiring@continua.ai"],
            "subject": "Hello World!!!",
            "timestamp": 1690569041,
            "message_content": "Body Content…",
        }
        client.post("/v1/emails", json=request_json)
        request_json["subject"] = "invalid"
        request_json["message_content"] = "invalid"
        client.post("/v1/emails", json=request_json)
        assert Email.select().count() == 2

        payload = {"keywords": "Hello World"}
        response = client.get("/v1/emails", params=payload)
        response_json = response.json()

        assert response.status_code == 200
        assert len(response_json) == 1

        assert response_json[0]["sender_email"] == response_json[0]["sender_email"]
        assert response_json[0]["receiver_email"] == response_json[0]["receiver_email"]
        assert (
            response_json[0]["cc_receiver_emails"]
            == response_json[0]["cc_receiver_emails"]
        )
        assert response_json[0]["subject"] == response_json[0]["subject"]
        assert response_json[0]["timestamp"] == response_json[0]["timestamp"]
        assert (
            response_json[0]["message_content"] == response_json[0]["message_content"]
        )

    field_to_search = ["after", "before"]

    @pytest.mark.parametrize("search_field", field_to_search)
    def test_search__addresses__correct_response(self, search_field, an_email):
        before_email = an_email(timestamp=10)
        after_email = an_email(timestamp=20)
        assert Email.select().count() == 2

        payload = {search_field: 15}
        response = client.get("/v1/emails", params=payload)
        response_json = response.json()

        assert response.status_code == 200
        assert len(response_json) == 1

        email = before_email if search_field == "before" else after_email
        assert response_json[0]["sender_email"] == email.sender_email
        assert response_json[0]["receiver_email"] == email.receiver_email
        assert response_json[0]["cc_receiver_emails"] == email.cc_receiver_emails.split(
            ", "
        )
        assert response_json[0]["subject"] == email.subject
        assert response_json[0]["timestamp"] == email.timestamp
        assert response_json[0]["message_content"] == email.message_content
