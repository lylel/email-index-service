from typing import List

from pydantic import BaseModel, field_serializer


class EmailArgs(BaseModel):
    sender: str
    recipient: str
    cc_recipients: List[str] | None = None
    subject: str | None = None
    timestamp: int
    message_content: str | None = None
    searchable_text: str | None = None

    @field_serializer("cc_recipients")
    def serialize_cc_recipients(self, cc_recipients: List[str]) -> str:
        return ", ".join(self.cc_recipients)
