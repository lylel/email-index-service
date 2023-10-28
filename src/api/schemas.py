from pydantic import BaseModel


class Email(BaseModel):
    sender_email: str
    receiver_email: str | None = None
    cc_receiver_emails: list[str | None]
    subject: str
    timestamp: int
    message_content: str
