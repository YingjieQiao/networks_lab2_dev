from typing import List, Optional

from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    email: str


class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int
    enrolled_students: List[Student] = []

    class Config:
        orm_mode = True

