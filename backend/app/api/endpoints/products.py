from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.security import require_manager_or_admin
from app.models import User
from app.schemas.product_schema import (
    ProductCreateManagerAdmin,
    ProductReadCustomer,
    ProductReadManagerAdmin,
    ProductUpdateAdmin,
)
from app.services.product_service import ProductService
from app.dependencies.services import get_product_service




# -------------------
# CUSTOMER ENDPOINTS
# -------------------

router_public = APIRouter(prefix="/products", tags=["Products - Public"])

@router_public.get("/", response_model=List[ProductReadCustomer])
async def list_products(product_service: ProductService = Depends(get_product_service)):
    products = await product_service.get_all_products()
    return products


@router_public.get("/{product_id}", response_model=ProductReadCustomer)
async def get_product(
    product_id: int, product_service: ProductService = Depends(get_product_service)
):
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# -------------------
# ADMIN ENDPOINTS
# -------------------

router_admin = APIRouter(prefix="/admin/products", tags=["Products - Admin"])

# Create new product
@router_admin.post(
    "/", response_model=ProductReadManagerAdmin, status_code=status.HTTP_201_CREATED
)
async def create_product(
    product_in: ProductCreateManagerAdmin,
    current_user: User = Depends(require_manager_or_admin),
    product_service: ProductService = Depends(get_product_service),
):

    product = await product_service.create_product(product_in)
    return product


# Update product info by id
@router_admin.put("/{product_id}", response_model=ProductReadManagerAdmin)
async def update_product(
    product_id: int,
    product_in: ProductUpdateAdmin,
    current_user: User = Depends(require_manager_or_admin),
    product_service: ProductService = Depends(get_product_service),
):

    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = await product_service.update_product(
        product, product_in.dict(exclude_unset=True)
    )
    return updated


# Delete product by id
@router_admin.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user: User = Depends(require_manager_or_admin),
    product_service: ProductService = Depends(get_product_service),
):
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await product_service.delete_product(product)
