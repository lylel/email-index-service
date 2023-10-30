from fastapi import APIRouter
from fastapi.params import Query

from src.api.schemas import EmailRequest, serialize_email, serialize_emails
from src.api.utils import parse_psv_query_string
from src.services.indexer import Indexer
from src.services.search_engine import SearchEngine

router = APIRouter(prefix="/v1/emails")


@router.post("/", response_model=EmailRequest)
def import_email(email: EmailRequest):
    return serialize_email(Indexer().ingest(email))


@router.get("/")
def search(
    # TODO: Can this be objectified into a Pydantic schema
    keywords: str
    | None = Query(
        None, title="Search Key Words", description="List of words separated by '+'"
    ),
    sender: str | None = None,
    recipient: str | None = None,
    sender_or_recipient: str | None = None,
    after: int | None = None,
    before: int | None = None,
):
    return serialize_emails(
        SearchEngine().search(
            keywords=parse_psv_query_string(keywords) if keywords else None,
            sender=sender,
            recipient=recipient,
            sender_or_recipient=sender_or_recipient,
            after=after,
            before=before,
        )
    )
