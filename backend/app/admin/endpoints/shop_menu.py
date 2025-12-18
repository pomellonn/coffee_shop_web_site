from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from core.security import require_admin
from models import User
from schemas.coffeeshop_schema import (
    CoffeeShopCreateAdmin,
    CoffeeShopReadCustomer,
    CoffeeShopReadManagerAdmin,
    CoffeeShopUpdateAdmin,
)
from services.coffeeshop_service import CoffeeShopService
from dependencies.services import get_coffee_shop_service
from fastapi import APIRouter

router = APIRouter()


# List all shops - Admin View
@router.get("/", response_model=List[CoffeeShopReadManagerAdmin])
async def list_shops_admin(
    shop_service: CoffeeShopService = Depends(get_coffee_shop_service),
    current_user: User = Depends(require_admin),
):
    shops = await shop_service.get_all_shops()
    return shops


# Get shop by id
@router.get("/{shop_id}", response_model=CoffeeShopReadManagerAdmin)
async def get_shop_admin(
    shop_id: int,
    shop_service: CoffeeShopService = Depends(get_coffee_shop_service),
    current_user: User = Depends(require_admin),
):
    shop = await shop_service.get_shop_by_id(shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Coffee shop not found")
    return shop


# Create new shop
@router.post(
    "/", response_model=CoffeeShopReadManagerAdmin, status_code=status.HTTP_201_CREATED
)
async def create_shop(
    shop_in: CoffeeShopCreateAdmin,
    current_user: User = Depends(require_admin),
    shop_service: CoffeeShopService = Depends(get_coffee_shop_service),
):
    shop = await shop_service.create_shop(shop_in)
    return shop


# Update shop by id
@router.put("/{shop_id}", response_model=CoffeeShopReadManagerAdmin)
async def update_shop(
    shop_id: int,
    shop_in: CoffeeShopUpdateAdmin,
    current_user: User = Depends(require_admin),
    shop_service: CoffeeShopService = Depends(get_coffee_shop_service),
):
    shop = await shop_service.get_shop_by_id(shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Coffee shop not found")

    updated_shop = await shop_service.update_shop(
        shop, shop_in.dict(exclude_unset=True)
    )
    return updated_shop


# Delete shop by id
@router.delete("/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shop(
    shop_id: int,
    current_user: User = Depends(require_admin),
    shop_service: CoffeeShopService = Depends(get_coffee_shop_service),
):
    shop = await shop_service.get_shop_by_id(shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Coffee shop not found")

    await shop_service.delete_shop(shop)
