from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.security import require_admin
from app.models import User
from app.schemas.product_attributes_schema import (
    ProductAttributesCreate,
    ProductAttributesReadAdminManager,
    ProductAttributesReadUser,
)
from app.services.product_attributes_service import ProductAttributesService
from app.dependencies.services import get_product_attributes_service


router = APIRouter(prefix="/products", tags=["product attributes"])


@router.get("/{product_id}/attributes", response_model=ProductAttributesReadUser)
async def get_product_attributes_for_user(
    product_id: int,
    svc: ProductAttributesService = Depends(get_product_attributes_service),
):
    return await svc.get_attributes_for_product_user(product_id)


@router.get("/admin/{product_id}/attribute-links", response_model=List[ProductAttributesReadAdminManager])
async def list_product_attribute_links_admin(
    product_id: int,
    svc: ProductAttributesService = Depends(get_product_attributes_service),
    current_user: User = Depends(require_admin),
):
    return await svc.list_links(product_id)


@router.post("/admin/attribute-links", response_model=ProductAttributesReadAdminManager, status_code=status.HTTP_201_CREATED)
async def create_product_attribute_link_admin(
    link_in: ProductAttributesCreate,
    svc: ProductAttributesService = Depends(get_product_attributes_service),
    current_user: User = Depends(require_admin),
):
    return await svc.add_link(link_in.product_id, link_in.option_id)


@router.delete("/admin/{product_id}/attribute-links/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_attribute_link_admin(
    product_id: int,
    option_id: int,
    svc: ProductAttributesService = Depends(get_product_attributes_service),
    current_user: User = Depends(require_admin),
):
    ok = await svc.delete_link(product_id, option_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Link not found")
    return None