from fastapi.testclient import TestClient

from ..app.main import app as application
from tests.assets.constants import students, courses

client = TestClient(application)

PUT_STUDENT_SUCCESS = students[0]
PUT_COURSE_SUCCESS = courses[0]



