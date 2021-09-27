from fastapi import Path
from fastapi.testclient import TestClient
import json, os

from ..app.main import app as application

client = TestClient(application)

UPLOAD_SUCCESS = "chinese_meme_1.png"


def test_upload():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "assets", "images", UPLOAD_SUCCESS)
    target_endpoint = "/image/" + UPLOAD_SUCCESS
    with open(path, "rb") as file:
        response = client.post(target_endpoint,
                               files={"uploaded_file": (UPLOAD_SUCCESS, file, "image/png")})
        assert response.status_code == 200


def test_download():
    target_endpoint = os.path.join("/image/", UPLOAD_SUCCESS)
    response = client.get(target_endpoint)
    print(response.text)
    assert response.status_code == 200
