from pydantic import BaseModel

from src.models.email import Email


class EmailRequest(BaseModel):
    sender_email: str
    receiver_email: str
    cc_receiver_emails: list[str] | None
    subject: str | None = None
    timestamp: int
    message_content: str | None = None


class SearchRequest(BaseModel):
    keywords: str | None = None
    sender_email: str | None = None
    receiver_email: str | None = None
    sender_or_recipient: str | None = None
    after: int | None = None
    before: int | None = None


class EmailResponse(BaseModel):
    sender_email: str
    receiver_email: str
    cc_receiver_emails: list[str] | None
    subject: str | None
    timestamp: int
    message_content: str | None

    class Config:
        from_attributes = True
        populate_by_name = True


def serialize_email(email: Email) -> dict:
    email.cc_receiver_emails = email.cc_receiver_emails.split(", ")
    return EmailResponse.model_validate(email).model_dump()


def serialize_emails(emails: list[Email]) -> list[dict]:
    return [serialize_email(email) for email in emails]
