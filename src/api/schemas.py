from pydantic import BaseModel, field_serializer


class EmailRequest(BaseModel):
    sender_email: str
    receiver_email: str
    cc_receiver_emails: list[str | None]
    subject: str | None = None
    timestamp: int
    message_content: str | None


class EmailResponse(BaseModel):
    sender: str
    recipient: str
    cc_recipients: str
    subject: str
    timestamp: int
    message_content: str

    class Config:
        from_attributes = True

    @field_serializer("cc_recipients")
    def serialize_cc_recipients(self, cc_recipients: str):
        return self.cc_recipients.split(", ")
