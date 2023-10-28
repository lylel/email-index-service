from typing import List

from pydantic import BaseModel, field_serializer


class EmailArgs(BaseModel):
    addressed_from: str
    addressed_to: str
    cc_recipients: List[str]
    actual_recipient: str
    subject: str
    timestamp: int
    message_content: str
    searchable_text: str

    @field_serializer("cc_recipients")
    def serialize_cc_recipients(self, cc_recipients: List[str]):
        return ", ".join(self.cc_recipients)
