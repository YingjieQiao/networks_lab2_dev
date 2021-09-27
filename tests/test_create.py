from fastapi.testclient import TestClient
import json

from ..app.main import app as application
from tests.assets.constants import students, courses

client = TestClient(application)

CREATE_STUDENT_SUCCESS = students[0]
CREATE_COURSE_SUCCESS = courses[0]


def test_create_course():
    response = client.post("/course", data=json.dumps(CREATE_COURSE_SUCCESS))
    assert response.status_code == 200


def test_create_student():
    response = client.post("/student", data=json.dumps(CREATE_STUDENT_SUCCESS))
    assert response.status_code == 200


