from fastapi.testclient import TestClient
import json, os

from ..app.main import app as application

client = TestClient(application)

UPLOAD_SUCCESS = "cat.png"


def test_upload():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", UPLOAD_SUCCESS)
    files = {"uploaded_file": (UPLOAD_SUCCESS, open(path, "rb"), "multipart/form-data")}
    response = client.post("/file", files=files, headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_download():
    target_endpoint = os.path.join("/file", UPLOAD_SUCCESS)
    response = client.get(target_endpoint, headers={"X-Token": "my_nonna"})
    # print(response.text)
    print(response)
    assert response.status_code == 200
