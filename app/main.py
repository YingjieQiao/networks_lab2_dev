from typing import List, Optional
import os, base64, shutil
from functools import wraps

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Request, Header
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
load_dotenv()

app = FastAPI()
SECRET_KEY = os.getenv("SECRET_KEY")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_request_header(x_token: str = Header(...)):
    if x_token != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# endpoints
@app.get("/heartbeat", dependencies=[Depends(check_request_header)], status_code=200)
def heartbeat():
    return "The connection is up"


@app.post("/course", dependencies=[Depends(check_request_header)],
          response_model=schemas.Course, status_code=200)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course=course)
    if db_course:
        raise HTTPException(status_code=400, detail="This course has already been created.")
    try:
        return crud.create_course(db=db, course=course)
    except:
        raise HTTPException(status_code=400, detail="Bad request body")


@app.delete("/course", dependencies=[Depends(check_request_header)],
            response_model=schemas.Course, status_code=200)
def delete_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    deleted_course = crud.delete_course(db, course)
    if deleted_course is None:
        raise HTTPException(status_code=404, detail="Trying to delete nonexistent rows.")
    return deleted_course


@app.post("/student", dependencies=[Depends(check_request_header)],
          response_model=schemas.Student, status_code=200)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student=student)
    if db_student:
        raise HTTPException(status_code=400, detail="This student has already been created.")
    return crud.create_student(db=db, student=student)


@app.delete("/student", dependencies=[Depends(check_request_header)],
            response_model=schemas.Student, status_code=200)
def delete_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    deleted_student = crud.delete_student(db, student)
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Trying to delete nonexistent rows.")
    return deleted_student


@app.put("/course/{course_id}/{student_id}", dependencies=[Depends(check_request_header)],
         response_model=schemas.Student, status_code=200)
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


@app.get("/course", dependencies=[Depends(check_request_header)],
         response_model=List[schemas.Course], status_code=200)
def get_course(db: Session = Depends(get_db)):
    try:
        courses = crud.get_all_course(db)
    except:
        raise HTTPException(status_code=500, detail="unexpected error in query")
    return courses


@app.get("/student", dependencies=[Depends(check_request_header)],
         response_model=List[schemas.Student], status_code=200)
def get_student(sort_by: Optional[str] = None, count: Optional[int] = None,
                offset: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        students = crud.get_all_student(db, sort_by, count, offset)
    except:
        raise HTTPException(status_code=500, detail="unexpected error in query")
    return students


@app.get("/course/{course_name}", dependencies=[Depends(check_request_header)],
         response_model=schemas.Course, status_code=200)
def get_course_by_name(course_name: str, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_name(db, course_name)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@app.get("/student/{student_name}", dependencies=[Depends(check_request_header)],
         response_model=schemas.Student, status_code=200)
def get_student_by_name(student_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_name(db, student_name)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.get("/course/byid/{course_id}", dependencies=[Depends(check_request_header)],
         response_model=schemas.Course, status_code=200)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@app.get("/student/byid/{student_id}", dependencies=[Depends(check_request_header)],
         response_model=schemas.Student, status_code=200)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.post("/file", dependencies=[Depends(check_request_header)], status_code=200)
def upload_image(uploaded_file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = uploaded_file.filename
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "object_store", filename)

    db_file = crud.get_file_row(db, filename)
    if db_file:
        raise HTTPException(status_code=400, detail="A file with the same filename already exists.")
    try:
        crud.create_file_row(db, filename)
    except:
        raise HTTPException(status_code=500, detail="database query error")

    try:
        with open(path, "wb+") as file_object:
            # practically, should be an object store service like AWS S3
            shutil.copyfileobj(uploaded_file.file, file_object)
    except:
        raise HTTPException(status_code=500, detail="writing to server disk error")

    return path


@app.get("/file/{filename}", dependencies=[Depends(check_request_header)], status_code=200)
def download_image(filename: str, db: Session = Depends(get_db)):
    db_file = crud.get_file_row(db, filename)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "object_store", filename)
    return FileResponse(path)


# http://127.0.0.1:8000/student/pullup_gpa/4.0/0.01
@app.put("/student/pullup_gpa/{threshold}/{delta}", dependencies=[Depends(check_request_header)], status_code=200)
def pullup_gpa(threshold: float, delta: float, db: Session = Depends(get_db)):
    try:
        db_students = crud.batch_update_student_gpa(db, threshold, delta)
        return db_students
    except:
        raise HTTPException(status_code=500, detail="server side error")


# cannot use plaintext, must use multipart/form-data
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

