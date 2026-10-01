# Library Management API

A REST API built using FastAPI and SQLite to manage library books and members.

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Swagger UI

## Features

* Book CRUD operations
* Member CRUD operations
* Unique ISBN validation
* Unique member email validation
* Input validation
* Search books by category and author
* Borrow books
* Return books
* Available quantity management
* Error handling
* Swagger API documentation

## API Endpoints

Books

* POST /books - Create a book
* GET /books - Get all books
* GET /books/{book_id} - Get book by ID
* PUT /books/{book_id} - Update book
* DELETE /books/{book_id} - Delete book

## Members

* POST /members - Create a member
* GET /members - Get all members
* GET /members/{member_id} - Get member by ID
* PUT /members/{member_id} - Update member
* DELETE /members/{member_id} - Delete member

## Borrow and Return

* POST /members/{member_id}/books/{book_id}/borrow
* POST /members/{member_id}/books/{book_id}/return

## Search

* GET /books?category=Programming
* GET /books?author=Robert

## Setup

Create and activate a virtual environment:

python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the application:

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

Database

The application uses SQLite with SQLAlchemy.

The database tables are created automatically when the application starts.

### Validation

The API validates:

* Book price must be greater than 0
* Available quantity must be 0 or greater
* ISBN must be unique
* Member email must be unique
* Required fields must be provided
* Email format must be valid

### HTTP Status Codes

* 200 - Successful request
* 201 - Resource created
* 204 - Resource deleted
* 400 - Invalid request or duplicate data
* 404 - Resource not found
* 422 - Validation error