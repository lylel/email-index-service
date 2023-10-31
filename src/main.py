from fastapi import FastAPI

from src.api import v1_emails
from src.db import db
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy

db.connect()
db.create_tables([Email, EmailCarbonCopy])

app = FastAPI()

app.include_router(v1_emails.router)
