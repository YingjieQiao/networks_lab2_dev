from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from . import models, schemas



# TODO: offset
# def get_courses(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Course).offset(skip).limit(limit).all()


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

# TODO: offset
# def get_students(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Student).offset(skip).limit(limit).all()


def add_student_to_course(db: Session, course: schemas.Course, student: schemas.Student):
    try:
        updated_student = db.query(models.Student).filter(models.Student.id == student.id).update("course_id", course.id)
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


def get_image_row(db: Session, name: str):
    return db.query(models.Image).filter(models.Image.name == name).first()


def create_image_row(db: Session, name: str):
    db_image = models.Student(name=name)
    # dont need to check duplicates
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return True


# def create_image(db: Session, name: str, encoded_img_string: str):
#     # TODO: check if exists
#     db_image = models.Image(name=name, image_base64str=encoded_img_string)
#     db.add(db_image)
#     db.commit()
#     db.refresh(db_image)
#
#     return db_image
#
#
# def get_image(db: Session, name: str):
#     return db.query(models.Image).filter(models.Image.name == name).first()

