import pytest

from src.db import db
from src.models.email import Email
from src.models.email_carbon_copy import EmailCarbonCopy


@pytest.fixture(scope="function")
def test_db():
    db.init(":memory:")
    db.connect()
    db.create_tables([Email, EmailCarbonCopy])
    yield
    db.drop_tables([Email, EmailCarbonCopy])
    db.close()
