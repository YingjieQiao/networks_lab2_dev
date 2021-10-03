from fastapi.testclient import TestClient
import json

from ..app.main import app as application


client = TestClient(application)


def test_get_student_all():
    response = client.get("/student", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_course_all():
    response = client.get("/course", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_sort_by():
    response = client.get("/student?sort_by=gpa", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_count():
    response = client.get("/student?count=3", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_offset():
    response = client.get("/student?offset=3", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_limit_sort_by():
    response = client.get("/student?sort_by=gpa&count=5", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_by_name():
    response = client.get("/student/Samwell%20Tarly", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_course_by_name():
    response = client.get("/course/Discrete%20Math", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_by_name_for_delete():
    response = client.get("/student/Samwell%20Tarly", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 404


def test_get_course_by_name_for_delete():
    response = client.get("/course/Discrete%20Math", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 404


def test_get_course_by_id():
    response = client.get("/course/byid/1", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_by_id():
    response = client.get("/student/byid/1", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200
