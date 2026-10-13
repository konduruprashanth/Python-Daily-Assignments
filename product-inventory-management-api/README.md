# Product Inventory Management API

A REST API built using FastAPI, SQLAlchemy ORM, and SQLite to manage products and categories.

## Technologies

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic

## Features

* Category and Product CRUD operations
* One-to-many relationships
* Request validation and error handling
* Product filtering and name search
* Inventory value calculation

## Setup

python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

## Run

python -m uvicorn app.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs

## Database

SQLite database: inventory.db

The database tables are created automatically when the application starts.