from src.models.email import Email
from src.profanity_remover.remover import ProfanityRemover
from src.repository.peewee_sqlite import Repository
from src.repository.schemas import SearchRequest
from src.services.utils import TextSearchOptimizer


class SearchEngine:
    def __init__(self, repository=None, search_optimizer=None):
        self._repository = repository
        self._search_optimizer = search_optimizer

    @property
    def repository(self):
        return self._repository or Repository

    @property
    def search_optimizer(self):
        return self._search_optimizer or TextSearchOptimizer

    def search(self, search_request: SearchRequest) -> list[Email]:
        if search_request.keywords:
            search_request.keywords = self.search_optimizer(
                text=search_request.keywords, sanitizer=ProfanityRemover
            ).optimize()
        return self.repository().find_all(search_request)
