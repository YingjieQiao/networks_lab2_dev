from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# endpoints
@app.get("/heartbeat", status_code=200)
def heartbeat():
    return "The connection is up"


@app.post("/course", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course=course)
    if db_course:
        raise HTTPException(status_code=400, detail="This course has already been created.")
    return crud.create_course(db=db, course=course)


@app.delete("/course", response_model=schemas.Course, status_code=200)
def delete_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    deleted_course = crud.delete_course(db, course)
    if deleted_course is None:
        raise HTTPException(status_code=404, detail="Trying to delete nonexistent rows.")
    return deleted_course


@app.post("/student", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student=student)
    if db_student:
        raise HTTPException(status_code=400, detail="This student has already been created.")
    return crud.create_student(db=db, student=student)


@app.delete("/student", response_model=schemas.Student)
def delete_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    deleted_student = crud.delete_student(db, student)
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Trying to delete nonexistent rows.")
    return deleted_student


@app.put("/course/{course_id}/student/", response_model=schemas.Student)
def add_student_to_course(
    course_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)
):
    return crud.create_student_by_course(db=db, student=student, course_id=course_id)


@app.get("/course_all", response_model=List[schemas.Course])
def get_all_course(db: Session = Depends(get_db)):
    try:
        courses = crud.get_all_course(db)
    except:
        raise HTTPException(status_code=500, detail="unexpected error in query")
    return courses


@app.get("/student_all", response_model=List[schemas.Student])
def get_all_course(db: Session = Depends(get_db)):
    try:
        students = crud.get_all_student(db)
    except:
        raise HTTPException(status_code=500, detail="unexpected error in query")
    return students


@app.get("/course/{course_id}", response_model=schemas.Course)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@app.get("/student/{student_id}", response_model=schemas.Student)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student





# @app.get("/course/", response_model=List[schemas.User])
# def read_course(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     course = crud.get_course(db, skip=skip, limit=limit)
#     return course

# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


#
# @app.post("/batch_course", response_model=schemas.Course)
# def create_batch_course(courses: List[schemas.CourseCreate], db: Session = Depends(get_db)):
#     res = []
#     for course in courses:
#         db_course = crud.get_course(db, course=course)
#         if db_course:
#             raise HTTPException(status_code=400, detail="This course has already been created.")
#         res.append(crud.create_course(db=db, course=course))
#     return res
