from fastapi.testclient import TestClient

from ..app.main import app as application
from tests.assets.constants import students, courses

client = TestClient(application)

PUT_STUDENT_SUCCESS = students[0]
PUT_COURSE_SUCCESS = courses[0]


def test_single_update():
    response = client.put("/course/1/1")
    print(response.text)
    assert response.status_code == 200


def test_batch_update():
    response = client.put("/student/pullup_gpa/4.0/0.5")
    print(response.text)
    assert response.status_code == 200
