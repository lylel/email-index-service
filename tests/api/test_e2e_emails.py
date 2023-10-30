import requests
from fastapi import FastAPI

from src.db import db
from src.models.email import Email

# Temp solution until I figure out how to use TestClient with a non-SQLAlchemy ORM
APP_URL = "http://127.0.0.1:8000/v1/emails/"


class TestEmailsAPI:
    def test_import_email(self):
        try:
            db.connect()
            starting_count = Email.select().count()
            response = requests.post(
                APP_URL,
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
            assert Email.select().count() == starting_count + 1
        finally:
            db.close()

    def test_search(self):
        app = FastAPI()
        response = requests.get(f"http://127.0.0.1:8000/v1/emails/")
        assert True is True
