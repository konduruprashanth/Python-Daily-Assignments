# RBAC Employee Management API

## Description

A REST API built using FastAPI, SQLite, SQLAlchemy, and Pydantic with JWT authentication and role-based access control.

## Features

* User registration and login
* JWT authentication
* Password hashing
* Admin, Manager, and Employee roles
* Employee CRUD operations
* Department, designation, and salary filters

## Technologies

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic
* JWT

## Run the Project

Install dependencies:

pip install -r requirements.txt

Start the server:

python -m uvicorn app.main:app --reload

Open Swagger UI: http://127.0.0.1:8000/docs