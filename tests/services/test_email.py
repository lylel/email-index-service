import pytest


@pytest.mark.usefixtures("test_db")
class TestEmailService:
    def test_create_email__(self):
        email = EmailService.ingest(
            addressed_from="people.ops@continua.ai",
            addressed_to="candidate@continua.ai",
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
            sender_or_recipient=None,
            after=0,
            before=None,
        )
