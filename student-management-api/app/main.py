from fastapi import FastAPI, HTTPException, Query
from sqlite3 import IntegrityError

from .database import create_table
from .schemas import StudentCreate, StudentResponse
from . import crud


app = FastAPI(title="Student Management API")


create_table()


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate):
    try:
        crud.create_student(student)
        return student

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Student ID or email already exists",
        )


@app.get("/students", response_model=list[StudentResponse])
def get_students(
    course: str | None = None,
    min_age: int | None = Query(default=None, ge=18),
    max_age: int | None = Query(default=None, le=60),
):
    students = crud.get_students(course, min_age, max_age)
    return students


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    student = crud.get_student(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate):
    existing_student = crud.get_student(student_id)

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    try:
        crud.update_student(student_id, student)
        return crud.get_student(student_id)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    existing_student = crud.get_student(student_id)

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    crud.delete_student(student_id)
    return None