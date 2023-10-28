from fastapi import APIRouter
from fastapi.params import Query

from src.api.schemas import Email, EmailResponse
from src.api.utils import parse_psv_query_string
from src.services.email import EmailService

router = APIRouter(prefix="/v1/emails")


@router.post("/", response_model=Email)
def import_email(email: Email):
    # TODO: return serialized ORM email
    processed_email = EmailService.import_email(
        addressed_from=email.sender_email,
        addressed_to=email.receiver_email,
        cc_recipients=email.cc_receiver_emails,
        subject=email.subject,
        timestamp=email.timestamp,
        message_content=email.message_content,
    )
    return email


# https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list
# Validate parameters
@router.get("/")
def search(
    keywords: str
    | None = Query(
        ..., title="Search Key Words", description="List of words separated by '+'"
    ),
    addressed_from: str | None = None,
    recipient: str | None = None,
    to_or_from: str | None = None,
    after: int | None = None,
    before: int | None = None,
):
    emails = EmailService.search(
        keywords=parse_psv_query_string(keywords),
        addressed_from=addressed_from,
        recipient=recipient,
        to_or_from_address=to_or_from,
        after=after,
        before=before,
    )

    return [
        {
            "sender_email": email.addressed_from,
            "receiver_email": email.addressed_to,
            "cc_recipients": email.cc_recipients,
            "subject": email.subject,
            "message_content": email.message_content,
        }
        for email in emails
    ]
