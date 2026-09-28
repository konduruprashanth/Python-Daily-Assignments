# Product Management API

A REST API built using Python, FastAPI, Pydantic, and SQLite for managing products.

## Features

* Create a product
* Get all products
* Get product by ID
* Update a product
* Delete a product
* Search products by category
* Validate price and quantity
* Prevent duplicate Product IDs
* Handle product-not-found errors

## Product Fields

* Product ID
* Product Name
* Category
* Price
* Quantity

## API Endpoints

Method	Endpoint	Description
POST	/products	Create product
GET	/products	Get all products
GET	/products/{product_id}	Get product by ID
PUT	/products/{product_id}	Update product
DELETE	/products/{product_id}	Delete product
GET	/products?category=Electronics	Filter by category

## Technologies Used

* Python
* FastAPI
* Pydantic
* SQLite
* Uvicorn

### Run the API

python -m uvicorn product-management-api.task:app --reload

Swagger documentation:

http://127.0.0.1:8000/docs

### Validation

* Product ID must be unique.
* Product name and category cannot be empty.
* Price must be greater than 0.
* Quantity must be greater than 0.
* Non-existing products return 404.