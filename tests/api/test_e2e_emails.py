import requests
from fastapi import FastAPI

from src.api.emails import search
from src.db import db
from src.models.email import Email

# Temp solution until I figure out how to use TestClient with a non-SQLAlchemy ORM
APP_URL = "http://127.0.0.1:8000/v1/emails/"


class TestEmailsAPI:
    def test_import_email(self):
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
