from fastapi import FastAPI

from src.api import emails
from src.db import db
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy

db.connect()
db.create_tables([Email, EmailCarbonCopy])

app = FastAPI()

app.include_router(emails.router)
