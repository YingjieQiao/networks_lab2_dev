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


def test_get_student_limit():
    response = client.get("/student?limit=3", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_offset():
    response = client.get("/student?offset=3", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_limit_sort_by():
    response = client.get("/student?sort_by=gpa&limit=5", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_student_by_name():
    response = client.get("/student/Walter%20White", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200


def test_get_course_by_name():
    response = client.get("/course/Intro%20to%20Algo", headers={"X-Token": "my_nonna"})
    print(response.text)
    assert response.status_code == 200
