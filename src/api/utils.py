# TODO: REMOVE?


def parse_psv_query_string(query_string: str) -> list:
    return query_string.replace(" ", "").split("+")
