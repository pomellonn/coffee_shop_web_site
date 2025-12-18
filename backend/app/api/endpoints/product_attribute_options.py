from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models import User
from core.security import require_admin
from schemas.product_attribute_options_schema import (
    ProductAttributeOptionsCreate,
    ProductAttributeOptionsUpdate,
    ProductAttributeOptionsRead
)

from services.product_attribute_options_service import ProductAttributeOptionsService
from dependencies.services import get_product_attribute_options_service

router = APIRouter(prefix="/product-attr-types-options", tags=["product attribute types options"])

@router.get("/admin", response_model=List[ProductAttributeOptionsRead])
async def list_product_attr_types_options(
    product_attr_options_service: ProductAttributeOptionsService = Depends(get_product_attribute_options_service),
    current_user: User = Depends(require_admin)
):
    options = await product_attr_options_service.get_all_product_attr_options()
    return options

@router.get("/admin/{option_id}", response_model=ProductAttributeOptionsRead)
async def get_product_options_value(
     option_id: int,
     product_attr_options_service: ProductAttributeOptionsService=Depends(get_product_attribute_options_service),
     current_user: User = Depends(require_admin),
):
    option=await product_attr_options_service.get_product_attribute_option_by_id(option_id)
    if not option:
        raise HTTPException(status_code=404, detail="Attribute type not found")
    return option

@router.post(
    "/admin",
    response_model=ProductAttributeOptionsRead,
    status_code=status.HTTP_201_CREATED
)

async def create_product_attr_option(
    option_in: ProductAttributeOptionsCreate,
    product_attr_options_service: ProductAttributeOptionsService = Depends(get_product_attribute_options_service),
    current_user: User = Depends(require_admin),
):
    try:
        option = await product_attr_options_service.create_product_attribute_option(option_in)
        return option
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/admin/{option_id}", response_model=ProductAttributeOptionsRead)
async def update_product_attr_option(
    option_id: int,
    option_in: ProductAttributeOptionsUpdate,
    product_attr_options_service: ProductAttributeOptionsService = Depends(get_product_attribute_options_service),
    current_user: User = Depends(require_admin),
):
    try:
        option = await product_attr_options_service.update_product_attribute_option(option_id, option_in)
        if not option:
            raise HTTPException(status_code=404, detail="Attribute option not found")
        return option
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/admin/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_attribute_option(
    option_id: int,
    product_attr_options_service: ProductAttributeOptionsService = Depends(get_product_attribute_options_service),
    current_user: User = Depends(require_admin),
):
    try:
        success = await product_attr_options_service.delete_product_attribute_option(option_id)
        if not success:
            raise HTTPException(status_code=404, detail="Attribute option not found")
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
