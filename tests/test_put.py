from fastapi.testclient import TestClient

from ..app.main import app as application

client = TestClient(application)



def test_single_update():
    response = client.put("/course/1/1", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_single_update_validate_course_not_found():
    response = client.put("/course/1000/1", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 404


def test_single_update_validate_student_not_found():
    response = client.put("/course/1/1000", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 404


def test_batch_update():
    response = client.put("/student/pullup_gpa/4.0/0.5", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200
