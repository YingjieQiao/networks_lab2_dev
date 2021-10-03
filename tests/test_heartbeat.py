from fastapi.testclient import TestClient

from ..app.main import app as application


client = TestClient(application)


def test_pass_verification():
    response = client.get("/heartbeat", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200
    assert response.text == '"The connection is up"'

def test_fail_verification():
    response = client.get("/heartbeat", headers={"X-Token": "sutd"})
    print(response.text)
    assert response.status_code == 401
