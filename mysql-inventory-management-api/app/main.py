from fastapi import FastAPI

from app.routers import (
    category_router,
    file_metadata_router,
    product_router,
    supplier_router,
)

app = FastAPI(
    title="Inventory Management API",
    description=("Manage products, categories, suppliers, and file uploads."),
    version="1.1.0",
)

app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(product_router)
app.include_router(file_metadata_router)
