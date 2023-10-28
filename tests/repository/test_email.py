import pytest

from src.repository.email import EmailRepository
from tests.fixtures.conftest import test_db, an_email


@pytest.mark.usefixtures("test_db")
class TestEmailRepository:
    def test_create(self):
        x = EmailRepository.create(
            sender="people.ops@continua.ai",
            recipient="candidate@continua.ai",
            subject="Welcome to Continua",
            timestamp=1690569041,
            message_content="Welcome! On your first day…",
            searchable_text="Welcome to Continua Welcome On your first day",
        )
        assert True is True

    def test_create_carbon_copies(self, an_email):
        email = an_email()
        copies = EmailRepository.create_carbon_copies(
            original=email, recipients=["xyz@mail.com"]
        )
        assert True is True

    def test_search(self, an_email):
        email = an_email()
        keywords = ["Continua", "Day"]
        assert EmailRepository.query(keywords=keywords) == [email]
