from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    gpa = Column(Float, unique=False)

    course_id = Column(Integer, ForeignKey('course.id'))
    # course = relationship("Student", back_populates="enrolled_students")


class Course(Base):
    """
    Many to One relationship. Students is many, Courses is one
    """

    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    enrolled_students = relationship("Student", backref="course")
    # enrolled_students = relationship("Student", back_populates="courses")
