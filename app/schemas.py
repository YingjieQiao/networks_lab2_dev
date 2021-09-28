from typing import List, Optional

from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    email: str
    gpa: float


class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    course_id: Optional[int]

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


class FileBase(BaseModel):
    name: str
    # image_base64str: str


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: int

    class Config:
        orm_mode = True
