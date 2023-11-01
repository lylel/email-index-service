from typing import List

from pydantic import BaseModel, field_serializer


class EmailArgs(BaseModel):
    sender_email: str
    receiver_email: str
    cc_receiver_emails: List[str] | None = None
    subject: str | None = None
    timestamp: int
    message_content: str | None = None
    searchable_text: str | None = None

    @field_serializer("cc_receiver_emails")
    def serialize_cc_receiver_emails(self, cc_receiver_emails: List[str]) -> str:
        return ", ".join(self.cc_receiver_emails)
