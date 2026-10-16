from fastapi import FastAPI

from app.routers import (
    category_router,
    product_router,
    supplier_router,
)

app = FastAPI(
    title="Inventory Management API",
    description="Manage products, categories, and suppliers.",
    version="1.0.0",
)

app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(product_router)