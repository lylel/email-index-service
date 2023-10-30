from fastapi import APIRouter
from fastapi.params import Query

from src.api.schemas import EmailRequest
from src.api.serializers import serialize_emails
from src.api.utils import parse_psv_query_string
from src.services.indexer import Indexer
from src.services.search_engine import SearchEngine

router = APIRouter(prefix="/v1/emails")

"""
RENAME -- this is specifically an email service, calling it Email is redundant
"""


@router.post("/", response_model=EmailRequest)  # TODO: CLEAN
def import_email(email: EmailRequest):
    processed_email = Indexer().ingest(email)
    return email


# https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list
# Validate parameters
@router.get("/")
def search(
    # Can this be objectified into a Pydantic schema
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
            addressed_from=sender,
            recipient=recipient,
            sender_or_recipient=sender_or_recipient,
            after=after,
            before=before,
        )
    )

    # return [
    #     {
    #         "sender_email": email.sender,
    #         "receiver_email": email.recipient,
    #         # "cc_recipients": email.cc_recipients,
    #         "subject": email.subject,
    #         "message_content": email.message_content,
    #     }
    #     for email in emails
    # ]
