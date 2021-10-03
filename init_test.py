from fastapi.testclient import TestClient
import json
from app.main import app as application

client = TestClient(application)


students = [
    {
        "name": "Walter White",
        "email": "walter_white@sutd.edu",
        "gpa": 5.3
    },
    {
        "name": "Jesse Pinkman",
        "email": "jess_pinkman@sutd.edu",
        "gpa": 0.5
    },
    {
        "name": "Gus String",
        "email": "gus_string@sutd.edu",
        "gpa": 4.5
    },
    {
        "name": "Hank Schrader",
        "email": "hank_schrader@sutd.edu",
        "gpa": 4.5
    },
    {
        "name": "Stannis Bar",
        "email": "stannis_bar@sutd.edu",
        "gpa": 2.5
    },
    {
        "name": "Jon Snow",
        "email": "jon_snow@sutd.edu",
        "gpa": 2.0
    },
    {
        "name": "Tyrion Lannister",
        "email": "tyrion_lanniester@sutd.edu",
        "gpa": 5.0
    },
    {
        "name": "Cersei Lannister",
        "email": "cersei_lannister@sutd.edu",
        "gpa": 1.0
    }
]

courses = [
    {
        "title": "Intro to Algo",
        "description": "leetcode"
    },
    {
        "title": "Digital World",
        "description": "use jupyter notebook"
    },
    {
        "title": "Computation Structures",
        "description": "most difficult module in ISTD"
    }
]


def populate_table():
    for student in students:
        client.post("/student", data=json.dumps(student),
                    headers={"X-Token": "my_nonna"})
    for course in courses:
        client.post("/course", data=json.dumps(course),
                    headers={"X-Token": "my_nonna"})


if __name__ == "__main__":
    populate_table()
