from fastapi.testclient import TestClient
import json

from ..app.main import app as application
from tests.assets.constants import students, courses

client = TestClient(application)

DELETE_STUDENT_SUCCESS = students[0]
DELETE_COURSE_SUCCESS = courses[0]


def test_delete_course():
    response = client.delete("/course", data=json.dumps(DELETE_COURSE_SUCCESS))
    assert response.status_code == 200


def test_delete_student():
    response = client.delete("/student", data=json.dumps(DELETE_STUDENT_SUCCESS))
    assert response.status_code == 200
