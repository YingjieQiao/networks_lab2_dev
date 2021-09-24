from sqlalchemy.orm import Session

from . import models, schemas


def get_course(db: Session, course_id: int):
    """
    get one course given course ID

    :param db: postgresql session
    :param course_id: int, primary key for Course
    :return: single Course object
    """

    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_course_by_title(db: Session, title: str):
    """
    get one course given course title

    :param db: postgresql session
    :param title: str, course title
    :return: single Course object
    """

    return db.query(models.Course).filter(models.Course.title == title).first()

# TODO: offset
# def get_courses(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course

# TODO: offset
# def get_students(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Student).offset(skip).limit(limit).all()


def create_student_by_course(db: Session, student: schemas.StudentCreate, course_id: int):
    db_student = models.Student(**student.dict(), course_id=course_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student
