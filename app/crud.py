from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from . import models, schemas



# TODO: offset
# def get_courses(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def create_student(db: Session, student: schemas.StudentCreate):
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

# TODO: offset
# def get_students(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Student).offset(skip).limit(limit).all()


def create_student_by_course(db: Session, student: schemas.StudentCreate, course_id: int):
    db_student = db.query(models.Student)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


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


def get_all_course(db: Session):
    try:
        return db.query(models.Course).all()
    except:
        raise Exception("unexpected error in query")


def get_all_student(db: Session):
    try:
        return db.query(models.Student).all()
    except:
        raise Exception("unexpected error in query")
