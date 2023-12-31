from fastapi import APIRouter, Depends

from src.api.schemas import (
    EmailRequest,
    serialize_email,
    serialize_emails,
    EmailResponse,
)
from src.api.schemas import SearchRequest
from src.services.indexer import Indexer
from src.services.search_engine import SearchEngine

router = APIRouter(prefix="/v1/emails")


@router.post("/", status_code=201, response_model=EmailResponse)
def import_email(email: EmailRequest):
    return serialize_email(Indexer().ingest(email=email))


@router.get("/", response_model=list[EmailResponse])
def search(search_request: SearchRequest = Depends(SearchRequest)):
    return serialize_emails(SearchEngine().search(search_request=search_request))
