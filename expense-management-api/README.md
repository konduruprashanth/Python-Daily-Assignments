# Expense Management API

A RESTful API built using FastAPI and SQLite to manage employee expenses and expense categories.

## Project Overview

The Expense Management API allows organizations to manage expense categories and employee expenses through a set of REST APIs.

The application supports complete CRUD operations for both categories and expenses, along with validation, filtering, date-range searches, category relationships, and total expense calculation.

## Technologies Used

* Python
* FastAPI – REST API framework
* SQLite – Database
* SQLAlchemy – ORM for database operations
* Pydantic – Request and response validation
* Uvicorn – ASGI server
* Swagger UI – API testing and documentation


## Validation Rules

The API validates all request data using Pydantic.

* Category ID must be unique
* Expense ID must be unique
* Category name must be unique
* Employee name is mandatory
* Category ID is mandatory
* Amount must be greater than 0
* Description is mandatory
* Expense date must be a valid date
* The selected category must exist before creating an expense

## Payment Methods

Only the following payment methods are accepted:

* Cash
* Card
* UPI
* Bank Transfer

## Expense Status

Only the following statuses are accepted:

* Pending
* Approved
* Rejected


## HTTP Status Codes

The API uses appropriate HTTP status codes for different situations.

Status Code	Meaning
200	Successful request
201	Resource created successfully
204	Resource deleted successfully
400	Bad request
404	Resource not found
409	Duplicate/conflicting resource
422	Validation error


## Running the Application

Start the FastAPI application using:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000


## Testing

The following scenarios should be tested:

Category Tests

* Create category
* Get all categories
* Get category by ID
* Update category
* Delete category
* Create duplicate category
* Get non-existing category

Expense Tests

* Create expense
* Get all expenses
* Get expense by ID
* Update expense
* Delete expense
* Filter by category
* Filter by status
* Filter by payment method
* Filter by date range
* Calculate total expenses

Validation Tests

* Create expense with a non-existing category
* Create expense with amount 0
* Create expense with negative amount
* Create expense with invalid payment method
* Create expense with invalid status
* Get a non-existing expense


### Learning Concepts

This project demonstrates the following concepts:

* FastAPI
* REST API development
* CRUD operations
* Pydantic validation
* SQLite database
* SQLAlchemy ORM
* Request body validation
* Path parameters
* Query parameters
* Response models
* Enum validation
* Date validation
* Filtering
* Date-range filtering
* Entity relationships
* Business logic
* Exception handling
* HTTP status codes
* Swagger UI
* Postman testing
