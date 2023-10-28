from fastapi.testclient import TestClient

from main import app


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

    {
        "sender_email": "people.ops@continua.ai",
        "receiver_email": "candidate@continua.ai",
        "cc_receiver_emails": ["hiring@continua.ai"],
        "subject": "Welcome to Continua",
        "timestamp": 1690569041,
        "message_content": "Welcome.  @! On  apple     your  ...     first day…",
    }
