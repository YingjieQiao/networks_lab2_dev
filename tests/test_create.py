from fastapi.testclient import TestClient
import json

from ..app.main import app as application

client = TestClient(application)

CREATE_STUDENT_SUCCESS = {
    "name": "Samwell Tarly",
    "email": "samwell_tarly@sutd.edu",
    "gpa": 5.0
}

CREATE_COURSE_SUCCESS = {
    "title": "Discrete Math",
    "description": "sutd doesnt teach"
}


CREATE_COURSE_FAIL_1 = {
    "title": "missing description"
}


def test_create_course_success():
    response = client.post("/course", data=json.dumps(CREATE_COURSE_SUCCESS),
                           headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_create_student_success():
    response = client.post("/student", data=json.dumps(CREATE_STUDENT_SUCCESS),
                           headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_create_student_fail_1():
    """
    same row already exists
    """

    response = client.post("/student", data=json.dumps(CREATE_STUDENT_SUCCESS),
                           headers={"X-Token": "my_nonna"})
    assert response.status_code == 400


def test_create_course_fail_1():
    response = client.post("/course", data=json.dumps(CREATE_COURSE_FAIL_1),
                           headers={"X-Token": "my_nonna"})
    assert response.status_code == 400




