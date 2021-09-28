from typing import List, Optional
import os, base64

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
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


@app.post("/course", response_model=schemas.Course, status_code=200)
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


@app.post("/student", response_model=schemas.Student, status_code=200)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student=student)
    if db_student:
        raise HTTPException(status_code=400, detail="This student has already been created.")
    return crud.create_student(db=db, student=student)


@app.delete("/student", response_model=schemas.Student, status_code=200)
def delete_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    deleted_student = crud.delete_student(db, student)
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Trying to delete nonexistent rows.")
    return deleted_student


@app.put("/course/{course_id}/{student_id}", response_model=schemas.Student, status_code=200)
def add_student_to_course(
    course_id: int, student_id: int, db: Session = Depends(get_db)
):
    db_student = crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not Found.")
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not Found.")
    try:
        return crud.add_student_to_course(db=db, course=db_course, student=db_student)
    except:
        raise HTTPException(status_code=500, detail="unexpected error in query.")


@app.get("/course", response_model=List[schemas.Course], status_code=200)
def get_course(db: Session = Depends(get_db)):
    try:
        courses = crud.get_all_course(db)
    except:
        raise HTTPException(status_code=500, detail="unexpected error in query")
    return courses


@app.get("/student", response_model=List[schemas.Student], status_code=200)
def get_student(sort_by: Optional[str] = None, limit: Optional[int] = None,
                offset: Optional[int] = None, db: Session = Depends(get_db),):
    try:
        students = crud.get_all_student(db, sort_by, limit, offset)
    except:
        raise HTTPException(status_code=500, detail="unexpected error in query")
    return students


@app.get("/course/{course_id}", response_model=schemas.Course, status_code=200)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@app.get("/student/{student_id}", response_model=schemas.Student, status_code=200)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.get("/course/{course_name}", response_model=schemas.Course, status_code=200)
def get_course_by_name(student_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_name(db, student_name)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.get("/student/{student_name}", response_model=schemas.Student, status_code=200)
def get_student_by_name(student_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_name(db, student_name)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.post("/image/{filename}", status_code=200)
def upload_image(filename: str, uploaded_file: bytes = File(...), db: Session = Depends(get_db)):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "object_store", filename)
    db_image = crud.get_image_row(db, filename)
    if db_image:
        raise HTTPException(status_code=400, detail="A file with the same filename already exists.")
    try:
        crud.create_image_row(db, filename)
    except:
        raise HTTPException(status_code=500, detail="database query error")

    try:
        with open(path, "wb+") as img:
            # practically, should be an object store service like AWS S3
            img.write(uploaded_file)
    except:
        raise HTTPException(status_code=500, detail="writing to servere disk error")

    return True



# cannot use plaintext, must use multimedia/form
# @app.post("/image/{filename}", response_model=schemas.Image, status_code=200)
# def upload_image_to_db(filename: str, db: Session = Depends(get_db)):
#     path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", filename)
#
#     with open(path, "rb") as img:
#         encoded_img_bytes = base64.b64encode(img.read())
#         encoded_img_string = encoded_img_bytes.decode('ascii')
#         db_image = crud.create_image(db, filename, encoded_img_string)
#
#     return db_image
#
#
# @app.get("/image/{filename}", status_code=200)
# def download_image_from_db(filename: str, db: Session = Depends(get_db)):
#     db_image = crud.get_image(db, filename)
#     if db_image is None:
#         raise HTTPException(status_code=404, detail="Image not found")
#     image_to_render = """<div><p>Rendered image</p><img src={0} alt={1} /></div>"""\
#         .format("data:image/jpeg;base64,"+db_image.image_base64str, db_image.name)
#     return image_to_render


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
