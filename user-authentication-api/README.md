# User Authentication API

A RESTful User Authentication API built using FastAPI, SQLite, SQLAlchemy, Pydantic, and Argon2 password hashing.

The API supports user registration, login, user management, role-based filtering, name search, and secure password changes.

## Features

* User registration
* User login
* Secure password hashing using Argon2
* Email validation
* Password minimum-length validation
* Unique email validation
* Role validation (Admin / User)
* User CRUD operations
* Role-based user filtering
* Name-based user search
* Password change functionality
* SQLite database
* Proper HTTP status codes and error handling
* Swagger API documentation

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Pydantic Email Validation
* pwdlib
* Argon2


## Validation

The API validates:

* Full name is required
* Email must have a valid format
* Email must be unique
* Password must contain at least 6 characters
* Role must be Admin or User
* User ID must exist for user-specific operations
* Current password must be correct before changing the password


Run the Application

Start the FastAPI server:

python -m uvicorn app.main:app --reload

The application will run at:

http://127.0.0.1:8000

Swagger Documentation

Open the following URL in a browser:

http://127.0.0.1:8000/docs

Swagger UI can be used to test all API endpoints.

The API was tested using Swagger UI for:

* Successful registration
* Duplicate email registration
* Invalid email
* Weak password
* Successful login
* Incorrect password
* Non-existing email
* Get all users
* Get user by ID
* Non-existing user
* Update user
* Duplicate email during update
* Role filtering
* Name search
* Password change
* Old password verification
* New password verification
* Password hash verification
* Successful user deletion
* Deleting a non-existing user

## Conclusion

This project demonstrates how to build a basic and secure user authentication and management API using FastAPI and SQLite.

It covers API development, database operations, request validation, password hashing, authentication, filtering, error handling, and RESTful CRUD operations.