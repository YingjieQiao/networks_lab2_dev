from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from . import models, schemas


def create_course(db: Session, course: schemas.CourseCreate):
    # TODO: check if exists
    db_course = models.Course(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def create_student(db: Session, student: schemas.StudentCreate):
    # TODO: check if exists
    db_student = models.Student(name=student.name, email=student.email, gpa=student.gpa)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def delete_course(db: Session, course: schemas.CourseCreate):
    affected_rows = get_course(db, course)
    if not affected_rows:
        raise Exception("Trying to delete nonexistent rows")
    db.delete(affected_rows)
    db.commit()

    return affected_rows


def delete_student(db: Session, student: schemas.StudentCreate):
    affected_rows = get_student(db, student)
    if not affected_rows:
        raise Exception("Trying to delete nonexistent rows")
    db.delete(affected_rows)
    db.commit()

    return affected_rows


def add_student_to_course(db: Session, course: schemas.Course, student: schemas.Student):
    try:
        updated_student = db.query(models.Student).filter(models.Student.id == student.id).first()
        updated_student.course_id = course.id
        db.commit()
    except:
        raise Exception("Failed to update database")

    return updated_student


def get_course(db: Session, course: schemas.CourseCreate):
    """
    get one course given a course object

    :param db: postgresql session
    :param course: schemas.CourseCreate, course to be created
    :return: single Course object
    """

    return db.query(models.Course).filter(or_(models.Course.title == course.title,
                                              models.Course.description == course.description)).first()


def get_student(db: Session, student: schemas.StudentCreate):
    return db.query(models.Student).filter(or_(models.Student.name == student.name,
                                               models.Student.email == student.email)).first()


def get_course_by_id(db: Session, course_id: int):
    """
    get one course given course ID

    :param db: postgresql session
    :param course_id: int, primary key for Course
    :return: single Course object
    """

    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_student_by_name(db: Session, student_name: str):
    return db.query(models.Student).filter(models.Student.name == student_name).first()


def get_all_course(db: Session):
    try:
        return db.query(models.Course).all()
    except:
        raise Exception("unexpected error in query")


def get_all_student(db: Session, sort_by: Optional[str] = None,
                    limit: Optional[int] = None, offset: Optional[int] = None):
    try:
        db_student = db.query(models.Student)
        if sort_by is not None:
            db_student = db_student.order_by(sort_by)
        if limit is not None:
            db_student = db_student.limit(limit)
        if offset is not None:
            db_student = db_student.offset(offset)
        return db_student.all()
    except:
        raise Exception("error in query")


def get_file_row(db: Session, name: str):
    return db.query(models.File).filter(models.File.name == name).first()


def create_file_row(db: Session, name: str):
    db_file = models.File(name=name)
    # dont need to check duplicates
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return True


def batch_update_student_gpa(db: Session, threshold: float, delta: float):
    updated_rows_count = db.query(models.Student).filter(models.Student.gpa <= threshold).\
                    update({models.Student.gpa : models.Student.gpa + delta})
    db.commit()

    return updated_rows_count

