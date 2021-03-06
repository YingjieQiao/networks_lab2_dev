from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.orm import relationship

from .database import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    gpa = Column(Float, unique=False, nullable=False)

    course_id = Column(Integer, ForeignKey('course.id'))
    # course = relationship("Student", back_populates="enrolled_students")


class Course(Base):
    """
    Many to One relationship. Students is many, Courses is one
    """

    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    enrolled_students = relationship("Student", backref="course")  # student.course = xxx
    # enrolled_students = relationship("Student", back_populates="courses")


class File(Base):
    """
    standalone table for images
    """

    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # image_base64str = Column(String)

