from app.routers.category_router import router as category_router
from app.routers.file_metadata_router import router as file_metadata_router
from app.routers.product_router import router as product_router
from app.routers.supplier_router import router as supplier_router

__all__ = [
    "category_router",
    "file_metadata_router",
    "product_router",
    "supplier_router",
]