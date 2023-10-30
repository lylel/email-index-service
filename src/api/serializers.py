from src.api.schemas import EmailResponse
from src.models.email import Email


def serialize_emails(emails: list[Email]) -> list[EmailResponse]:
    return [EmailResponse.model_validate(email).model_dump() for email in emails]
