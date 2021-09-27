from fastapi.testclient import TestClient

from ..app.main import app as application


client = TestClient(application)


def test_read_main():
    response = client.get("/heartbeat")
    assert response.status_code == 200
    assert response.text == '"The connection is up"'

