from fastapi.testclient import TestClient
from fastapi import HTTPException
import json
import pytest
from unittest import mock
from unittest.mock import patch
from requests import HTTPError

from ..app.main import app as application

client = TestClient(application)

DELETE_STUDENT_SUCCESS = {
    "name": "Samwell Tarly",
    "email": "samwell_tarly@sutd.edu",
    "gpa": 5.0
}

DELETE_COURSE_SUCCESS = {
    "title": "Discrete Math",
    "description": "sutd doesnt teach"
}


def test_delete_course():
    response = client.delete("/course", data=json.dumps(DELETE_COURSE_SUCCESS),
                             headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_delete_student():
    response = client.delete("/student", data=json.dumps(DELETE_STUDENT_SUCCESS),
                             headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_delete_course_validate():
    response = client.delete("/course", data=json.dumps(DELETE_COURSE_SUCCESS),
                             headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 404


def test_delete_student_validate():
    response = client.delete("/student", data=json.dumps(DELETE_STUDENT_SUCCESS),
                             headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 404
