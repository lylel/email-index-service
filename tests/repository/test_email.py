import pytest

from src.repository.email import EmailSQLiteRepository


@pytest.mark.usefixtures("test_db")
class TestEmailRepository:
    def test_create(self):
        x = EmailSQLiteRepository.save(
            addressed_from="people.ops@continua.ai",
            addressed_to="candidate@continua.ai",
            subject="Welcome to Continua",
            timestamp=1690569041,
            message_content="Welcome! On your first day…",
            searchable_text="Welcome to Continua Welcome On your first day",
        )
        assert True is True

    def test_create_carbon_copies(self, an_email):
        email = an_email()
        copies = EmailSQLiteRepository.create_carbon_copies(
            original=email, recipients=["xyz@mail.com"]
        )
        assert True is True

    def test_search(self, an_email):
        email = an_email()
        keywords = ["Continua", "Day"]
        assert EmailSQLiteRepository.query(keywords=keywords) == [email]
