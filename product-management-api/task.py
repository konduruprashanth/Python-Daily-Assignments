import sqlite3

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()


def get_connection():
    connection = sqlite3.connect("products.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL CHECK(price > 0),
            quantity INTEGER NOT NULL CHECK(quantity > 0)
        )
        """
    )

    connection.commit()
    connection.close()


create_table()


class Product(BaseModel):
    id: int
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


@app.post("/products", status_code=201)
def create_product(product: Product):
    connection = get_connection()

    existing_product = connection.execute(
        "SELECT id FROM products WHERE id = ?",
        (product.id,),
    ).fetchone()

    if existing_product:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="Product ID already exists",
        )

    connection.execute(
        """
        INSERT INTO products (id, name, category, price, quantity)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            product.id,
            product.name,
            product.category,
            product.price,
            product.quantity,
        ),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Product created successfully",
        "product": product,
    }


@app.get("/products")
def get_products(category: str | None = Query(default=None)):
    connection = get_connection()

    if category:
        products = connection.execute(
            "SELECT * FROM products WHERE category = ?",
            (category,),
        ).fetchall()
    else:
        products = connection.execute(
            "SELECT * FROM products"
        ).fetchall()

    connection.close()

    return [dict(product) for product in products]


@app.get("/products/{product_id}")
def get_product(product_id: int):
    connection = get_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    connection.close()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return dict(product)


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    connection = get_connection()

    existing_product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if existing_product is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if product.id != product_id:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="Product ID cannot be changed",
        )

    connection.execute(
        """
        UPDATE products
        SET name = ?, category = ?, price = ?, quantity = ?
        WHERE id = ?
        """,
        (
            product.name,
            product.category,
            product.price,
            product.quantity,
            product_id,
        ),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Product updated successfully",
        "product": product,
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    connection = get_connection()

    existing_product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if existing_product is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    connection.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Product deleted successfully"
    }