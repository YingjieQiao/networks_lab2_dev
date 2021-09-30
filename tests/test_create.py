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


def test_create_course():
    response = client.post("/course", data=json.dumps(CREATE_COURSE_SUCCESS),
                           headers={"X-Token": "my_nonna"})
    assert response.status_code == 200


def test_create_student():
    response = client.post("/student", data=json.dumps(CREATE_STUDENT_SUCCESS),
                           headers={"X-Token": "my_nonna"})
    assert response.status_code == 200


