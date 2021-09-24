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
@app.post("/course/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_title(db, title=course.title)
    if db_course:
        raise HTTPException(status_code=400, detail="This course has already been created.")
    return crud.create_course(db=db, course=course)


# @app.get("/course/", response_model=List[schemas.User])
# def read_course(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     course = crud.get_course(db, skip=skip, limit=limit)
#     return course


@app.get("/course/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@app.post("/course/{course_id}/students/", response_model=schemas.Student)
def create_student_by_course(
    course_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)
):
    return crud.create_student_by_course(db=db, student=student, course_id=course_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
