from pydantic import BaseModel, Field

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
    sender: str | None = None
    recipient: str | None = None
    sender_or_recipient: str | None = None
    after: int | None = None
    before: int | None = None


class EmailResponse(BaseModel):
    sender_email: str = Field(alias="sender")
    receiver_email: str = Field(alias="recipient")
    cc_receiver_emails: list[str] | None = Field(alias="cc_recipients")
    subject: str | None
    timestamp: int
    message_content: str | None

    class Config:
        from_attributes = True
        populate_by_name = True


def serialize_email(email: Email) -> dict:
    email.cc_recipients = email.cc_recipients.split(", ")
    return EmailResponse.model_validate(email).model_dump()


def serialize_emails(emails: list[Email]) -> list[dict]:
    return [serialize_email(email) for email in emails]
