from src.api.schemas import EmailRequest
from src.models.email import Email
from src.repository.peewee_sqlite import Repository
from src.services.preprocessor import PreProcessor


class Indexer:
    def __init__(self, preprocessor=None, repository=None):
        self._preprocessor = preprocessor
        self._repository = repository

    @property
    def preprocessor(self):
        return self._preprocessor or PreProcessor

    @property
    def repository(self):
        return self._repository or Repository

    def ingest(self, email: EmailRequest) -> Email:
        email_args = self.preprocessor().prepare(email=email)
        return self.repository().add_email_with_carbon_copies(email_args=email_args)
