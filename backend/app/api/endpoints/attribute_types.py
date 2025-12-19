from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models import User
from app.core.security import require_admin
from app.schemas.attribute_types_schema import (
    AttributeTypeCreateManagerAdmin,
    AttributeTypeUpdateManagerAdmin,
    AttributeTypeRead
)
from app.services.attribute_types_service import AttributeTypesService
from app.dependencies.services import get_attribute_types_service


# ---------------------------
# ADMIN ENDPOINTS
# ---------------------------

router_admin = APIRouter(prefix="/admin/attribute-types", tags=["Attribute types - Admin"])


# List all attribute types
@router_admin.get("/", response_model=List[AttributeTypeRead])
async def list_attribute_types_admin(
    attribute_types_service: AttributeTypesService = Depends(get_attribute_types_service),
    current_user: User = Depends(require_admin),
):
    types = await attribute_types_service.get_all_attribute_types()
    return types

# Get attribute by id
@router_admin.get("/{type_id}", response_model=AttributeTypeRead)
async def get_attribute_type_admin(
    type_id: int, 
    attribute_types_service: AttributeTypesService=Depends(get_attribute_types_service),
    current_user: User = Depends(require_admin),
):
    attr_type= await attribute_types_service.get_attribute_type_by_id(type_id)
    if not attr_type:
        raise HTTPException(status_code=404, detail="Attribute type not found")
    return attr_type

# Create new type
@router_admin.post(
    "/", 
    response_model=AttributeTypeRead, 
    status_code=status.HTTP_201_CREATED
)
async def create_attribute_type(
    type_in: AttributeTypeCreateManagerAdmin,
    current_user: User = Depends(require_admin), 
    attribute_types_service: AttributeTypesService = Depends(get_attribute_types_service),
):
    try:
        attr_type = await attribute_types_service.create_attribute_type(type_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return attr_type


@router_admin.put("/{type_id}", response_model=AttributeTypeRead)
async def update_attribute_type(
    type_id:int,
    type_in: AttributeTypeUpdateManagerAdmin,
    current_user: User = Depends(require_admin),
    attribute_types_service: AttributeTypesService = Depends(get_attribute_types_service),
):
    attr_type = await attribute_types_service.get_attribute_type_by_id(type_id)
    if not attr_type:
        raise HTTPException(status_code=404, detail="Attribute type not found")
    updated_type= await attribute_types_service.update_attribute_type(type_id, type_in)
    return updated_type


@router_admin.delete("/admin/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute_type(
    type_id: int,
    current_user: User = Depends(require_admin),
    attribute_types_service: AttributeTypesService=Depends(get_attribute_types_service)
):
    attr_type= await attribute_types_service.get_attribute_type_by_id(type_id)
    if not attr_type:
        raise HTTPException(status_code=404, detail="Attribute type not found")
    await attribute_types_service.delete_attribute_type(type_id)
    return None