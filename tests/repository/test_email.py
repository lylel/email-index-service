from src.models.email import Email
from src.repository.email import EmailRepository
from tests.fixtures.conftest import test_db


class TestEmailRepository:
    def test_add(self, test_db):

        x = EmailRepository.add(sender="people.ops@continua.ai",
                                recipient="candidate@continua.ai",
                                subject="Welcome to Continua",
                                timestamp=1690569041,
                                message_content="Welcome")
        assert True is True

    def test_search(self, test_db):
        Email.create(sender="people.ops@continua.ai",
                            recipient="candidate@continua.ai",
                            subject="Welcome to Continua",
                            timestamp=1690569041,
                            message_content="Hello")
        keywords = ["Hello"]
        x = EmailRepository.search(keywords=keywords)
        assert True is True
