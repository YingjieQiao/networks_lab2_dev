from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

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
