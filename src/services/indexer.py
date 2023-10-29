from src.api.schemas import Email
from src.repository.peewee_sqlite import SQLiteRepository
from src.services.preprocessor import PreProcessor


class Indexer:
    def __init__(self, email: Email, preprocessor=None, repository=None):
        self._email = email
        self._preprocessor = preprocessor
        self._repository = repository

    @property
    def email(self):
        return self._email

    @property
    def preprocessor(self):
        return self._preprocessor or PreProcessor

    @property
    def repository(self):
        return self._repository or SQLiteRepository

    def ingest(self):
        email_args = self.preprocessor(email=self.email).prepare()
        return self.repository().create_with_carbon_copies(email_args)
