from src.models.email import Email
from src.profanity_remover_v1.remover import ProfanityRemover
from src.repository.peewee_sqlite import Repository, SearchRequest
from src.services.text_search_optimizer import TextSearchOptimizer


class SearchEngine:
    def __init__(self, repository=None, search_optimizer=None, sanitizer=None):
        self._repository = repository
        self._search_optimizer = search_optimizer
        self._sanitizer = sanitizer

    @property
    def repository(self):
        return self._repository or Repository

    @property
    def search_optimizer(self):
        return self._search_optimizer or TextSearchOptimizer

    @property
    def sanitizer(self):
        return self._sanitizer or ProfanityRemover

    def search(self, search_request: SearchRequest) -> list[Email]:
        if search_request.keywords:
            search_request.keywords = self.search_optimizer(
                text=search_request.keywords, sanitizer=self.sanitizer
            ).optimize()
        return self.repository().find_all(search_request)
