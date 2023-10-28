from fastapi import FastAPI

from src.api import email
from src.db import db
from src.models.email import Email

db.connect()
db.create_tables([Email])

app = FastAPI()

app.include_router(email.router)
