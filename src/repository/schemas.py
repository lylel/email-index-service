from pydantic import BaseModel


class SearchRequest(BaseModel):
    keywords: list[str] = (None,)
    sender: str = (None,)
    recipient: str = (None,)
    sender_or_recipient: str = (None,)
    after: int = (None,)
    before: int = (None,)
