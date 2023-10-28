from pydantic import BaseModel


class Email(BaseModel):
    sender_email: str
    receiver_email: str
    cc_receiver_emails: list[str | None]
    subject: str | None = None
    timestamp: int
    message_content: str | None


class EmailResponse(BaseModel):
    sender_email: "addressed_from"
    receiver_email: "addressed_to"
    cc_receiver_emails: str
    actual_recipient: str
    subject: str | None = None
    timestamp: int
    message_content: str | None

    class Config:
        from_attributes = True
        #

    # @property
    # def cc_receiver_emails(self):
    #     return
