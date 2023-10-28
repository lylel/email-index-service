from src.api.utils import parse_psv_query_string


def test_parse_psv_query_string__list_separated_by_plus_delimitation():
    assert parse_psv_query_string("Hello+World+Bye") == ["Hello", "World", "Bye"]


def test_parse_psv_query_string__removes_white_spaces():
    assert parse_psv_query_string(" Hello  +  World    + Bye  ") == [
        "Hello",
        "World",
        "Bye",
    ]
