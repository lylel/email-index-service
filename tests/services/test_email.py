import pytest

from src.services.email import EmailService


@pytest.mark.usefixtures("test_db")
class TestEmailService:
    def test_create_email__(self):
        email = EmailService.import_email(
            sender="people.ops@continua.ai",
            recipient="candidate@continua.ai",
            cc_recipients=["hiring@continua.ai"],
            subject="Welcome to Continua",
            timestamp=1690569041,
            message_content="Welcome! On your first day…",
        )

    def test_search_email__(self, an_email):
        imported_email = an_email()

        EmailService.search(
            keywords=["Day", "Welcome", "On"],
            sender="people.ops@continua.ai",
            recipient="candidate@continua.ai",
            to_or_from_address=to_or_from,
            after=after,
            before=before,
        )
