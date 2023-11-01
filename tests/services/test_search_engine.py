import pytest

from src.api.schemas import SearchRequest
from src.services.search_engine import SearchEngine
from tests.conftest import test_db, an_email


@pytest.mark.usefixtures("test_db")
class TestSearchEngine:
    def test_search__keyword_search_single_match(self, an_email):
        email = an_email()
        search_request = SearchRequest(keywords="Hello World")
        results = SearchEngine().search(search_request)

        assert results[0] == email

    def test_search__keyword_search_multiple_matches(self, an_email):
        email_1, email_2, email_3 = an_email(), an_email(), an_email()

        search_request = SearchRequest(keywords="Hello World")
        results = SearchEngine().search(search_request)

        assert len(results) == 3
        assert results[0] == email_1
        assert results[1] == email_2
        assert results[2] == email_3

    def test_search__keyword_search_no_match(self, an_email):
        email = an_email()
        search_request = SearchRequest(keywords="this can't be found anywhere")

        assert not SearchEngine().search(search_request)

    def test_search__before_search_single_match(self, an_email):
        email = an_email(timestamp=10)
        search_request = SearchRequest(before=15)
        results = SearchEngine().search(search_request)

        assert results[0] == email

    def test_search__before_search_multiple_matches(self, an_email):
        email_1, email_2, email_3 = (
            an_email(timestamp=10),
            an_email(timestamp=12),
            an_email(timestamp=14),
        )

        search_request = SearchRequest(before=15)
        results = SearchEngine().search(search_request)

        assert len(results) == 3
        assert results[0] == email_1
        assert results[1] == email_2
        assert results[2] == email_3

    def test_search__before_search_no_match(self, an_email):
        an_email(timestamp=10)
        search_request = SearchRequest(before=9)
        assert not SearchEngine().search(search_request)

    def test_search__after_search_single_match(self, an_email):
        email = an_email(timestamp=15)
        search_request = SearchRequest(after=10)
        results = SearchEngine().search(search_request)

        assert results[0] == email

    def test_search__before_after_multiple_matches(self, an_email):
        email_1, email_2, email_3 = (
            an_email(timestamp=10),
            an_email(timestamp=12),
            an_email(timestamp=14),
        )

        search_request = SearchRequest(after=5)
        results = SearchEngine().search(search_request)

        assert len(results) == 3
        assert results[0] == email_1
        assert results[1] == email_2
        assert results[2] == email_3

    def test_search__after_search_no_match(self, an_email):
        an_email(timestamp=10)
        search_request = SearchRequest(after=15)
        assert not SearchEngine().search(search_request)

    def test_search__sender_email_search_single_match(self, an_email):
        email = an_email(sender_email="bob@yahoo.com")
        search_request = SearchRequest(sender_email=email.sender_email)
        results = SearchEngine().search(search_request)

        assert results[0].sender_email == email.sender_email

    def test_search__sender_email_multiple_matches(self, an_email):
        address = "bob@yahoo.com"
        email_1, email_2, email_3 = (
            an_email(sender_email=address),
            an_email(sender_email=address),
            an_email(sender_email=address),
        )

        search_request = SearchRequest(sender_email=email_1.sender_email)
        results = SearchEngine().search(search_request)

        assert len(results) == 3
        assert results[0] == email_1
        assert results[1] == email_2
        assert results[2] == email_3

    def test_search__sender_email_search_no_match(self, an_email):
        an_email(sender_email="bob@yahoo.com")
        search_request = SearchRequest(sender_email="joe@excite.com")
        assert not SearchEngine().search(search_request)

    def test_search__receiver_email_search_single_match(self, an_email):
        email = an_email(receiver_email="bob@yahoo.com")
        search_request = SearchRequest(receiver_email=email.receiver_email)
        results = SearchEngine().search(search_request)

        assert results[0].receiver_email == email.receiver_email

    def test_search__receiver_email_multiple_matches(self, an_email):
        address = "bob@yahoo.com"
        email_1, email_2, email_3 = (
            an_email(receiver_email=address),
            an_email(receiver_email=address),
            an_email(receiver_email=address),
        )

        search_request = SearchRequest(receiver_email=email_1.receiver_email)
        results = SearchEngine().search(search_request)

        assert len(results) == 3
        assert results[0] == email_1
        assert results[1] == email_2
        assert results[2] == email_3

    def test_search__receiver_email_search_no_match(self, an_email):
        an_email(receiver_email="bob@yahoo.com")
        search_request = SearchRequest(receiver_email="joe@excite.com")
        assert not SearchEngine().search(search_request)

    def test_search__sender_or_recipient_search_single_match(self, an_email):
        email = an_email(receiver_email="bob@yahoo.com")
        search_request = SearchRequest(sender_or_recipient=email.receiver_email)
        results = SearchEngine().search(search_request)

        assert results[0].receiver_email == email.receiver_email

    def test_search__sender_or_recipient_multiple_matches(self, an_email):
        address = "bob@yahoo.com"
        email_1, email_2 = an_email(receiver_email=address), an_email(
            sender_email=address
        )

        search_request = SearchRequest(sender_or_recipient=email_1.receiver_email)
        results = SearchEngine().search(search_request)

        assert len(results) == 2
        assert results[0] == email_1
        assert results[1] == email_2

    def test_search__sender_or_recipient_search_no_match(self, an_email):
        an_email(receiver_email="bob@yahoo.com")
        an_email(sender_email="bob@yahoo.com")

        search_request = SearchRequest(sender_or_recipient="joe@excite.com")
        assert not SearchEngine().search(search_request)
