import pytest

from src.api.schemas import SearchRequest, serialize_emails
from src.services.search_engine import SearchEngine
from tests.conftest import test_db, an_email


@pytest.mark.usefixtures("test_db")
class TestSearchEngine:
    def test_search(self, an_email):
        an_email()
        search_request = SearchRequest(keywords="aaaa")
        results = SearchEngine().search(search_request)
        x = serialize_emails(results)
        assert True
