from fastapi.testclient import TestClient
import json

from ..app.main import app as application
# from tests.assets.constants import students, courses

client = TestClient(application)

CREATE_STUDENT_SUCCESS = {
    "name": "Walter White",
    "email": "walter_white@sutd.edu",
    "gpa": 5.3
}

CREATE_COURSE_SUCCESS = {
    "title": "Intro to Algo",
    "description": "leetcode"
}


CREATE_COURSE_FAIL_1 = {
    "title": "discrete math"
}


def test_create_course_success():
    response = client.post("/course", data=json.dumps(CREATE_COURSE_SUCCESS),
                           headers={"X-Token": "my_nonna"})
    assert response.status_code == 200


def test_create_student_success():
    response = client.post("/student", data=json.dumps(CREATE_STUDENT_SUCCESS),
                           headers={"X-Token": "my_nonna"})
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




