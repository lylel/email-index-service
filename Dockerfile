FROM ubuntu:latest

FROM python:3.11.0-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY src /app/src/

COPY bootstrap.py /app/bootstrap.py

COPY emails.json /app/emails.json

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
