from pydantic import BaseModel


class SearchRequest(BaseModel):
    keywords: list[str] | None = None
    sender: str | None = None
    recipient: str | None = None
    sender_or_recipient: str | None = None
    after: int | None = None
    before: int | None = None
