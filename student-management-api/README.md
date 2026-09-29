# Student Management API

A REST API built using FastAPI and SQLite to manage student records.

## Features

* Create a student
* View all students
* View a student by ID
* Update a student
* Delete a student
* Search students by course
* Filter students by age
* Email validation
* Phone number validation
* Unique Student ID and Email
* Proper error handling
* Swagger API documentation

## Technologies Used

* Python
* FastAPI
* SQLite
* Pydantic
* Uvicorn

## Project Structure

```text
student-management-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── student.db
├── requirements.txt
└── README.md

How to Run

Create and activate the virtual environment:

python -m venv venv
venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Start the server:

uvicorn app.main:app --reload

Open Swagger:

http://127.0.0.1:8000/docs

API Endpoints

Method	Endpoint	Description
POST	/students	Create a student
GET	/students	Get all students
GET	/students/{student_id}	Get student by ID
PUT	/students/{student_id}	Update a student
DELETE	/students/{student_id}	Delete a student

Filters

GET /students?course=Python
GET /students?min_age=20&max_age=30