from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.orm import relationship

from .database import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    gpa = Column(Float, unique=False)

    course_id = Column(Integer, ForeignKey('course.id'))
    # course = relationship("Student", back_populates="enrolled_students")


class Course(Base):
    """
    Many to One relationship. Students is many, Courses is one
    """

    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

    enrolled_students = relationship("Student", backref="course")  # student.course = xxx
    # enrolled_students = relationship("Student", back_populates="courses")


class Image(Base):
    """
    standalone table for images
    """

    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # image_base64str = Column(String)

