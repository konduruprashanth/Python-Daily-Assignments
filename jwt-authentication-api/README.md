# JWT Authentication API

## Overview

The JWT Authentication API is a RESTful application developed using FastAPI, SQLAlchemy, Pydantic, and SQLite. It provides secure user registration, login, JWT-based authentication, and task management.
The API ensures that users can access and manage only their own tasks using a valid JWT access token.

## Features

* User registration with unique email validation
* Password hashing using bcrypt
* User login with email and password
* JWT access token generation and validation
* Protected endpoints using OAuth2 Bearer authentication
* Retrieve logged-in user details
* Create, read, update, and delete tasks
* Retrieve tasks assigned to the logged-in user
* Filter tasks by status and priority
* Mark tasks as completed
* SQLite database integration
* Pydantic request validation
* Appropriate HTTP status codes and error handling
* Interactive API documentation using Swagger UI

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT (JSON Web Tokens)
* bcrypt
* OAuth2 Password Bearer
* Uvicorn
* Swagger UI


The SQLite database is generated locally when the application runs and should not be committed to Git.

## Run the application

python -m uvicorn app.main:app --reload

The application runs locally at:

http://127.0.0.1:8000

API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

Alternative API documentation:

http://127.0.0.1:8000/redoc

## Testing

Use Swagger UI or Postman to test the APIs.

Recommended test cases:

1. Register a new user.
2. Register with a duplicate email.
3. Log in with valid credentials.
4. Log in with an incorrect password.
5. Log in with a non-existing email.
6. Access a protected endpoint with a valid token.
7. Access a protected endpoint without a token.
8. Access a protected endpoint with an invalid token.
9. Retrieve the logged-in user’s details.
10. Create, retrieve, update, and delete tasks.
11. Attempt to access another user’s task.
12. Filter tasks by status and priority.
13. Mark a task as completed.


## Database

The application uses SQLite with SQLAlchemy ORM to store user and task information.
The database file is created locally when the application starts.
