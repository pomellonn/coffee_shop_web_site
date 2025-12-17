from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from core.security import require_manager_or_admin, require_admin, require_manager
from models import User
from schemas.shopmenu_schema import (
    ShopMenuCreateAdmin,
    ShopMenuReadCustomer,
    ShopMenuReadManagerAdmin,
    ShopMenuUpdateManager,
    ShopMenuUpdateAdmin,
    ShopMenuCreateManager,
)
from services.shopmenu_service import ShopMenuService
from dependencies.services import get_shop_menu_service


# -----------------------------
# CUSTOMER ENDPOINTS
# -----------------------------

router_public = APIRouter(prefix="/menu", tags=["Shop menu - Public"])


# Get shop menu items
@router_public.get("/{shop_id}", response_model=List[ShopMenuReadCustomer])
async def get_shop_menu(
    shop_id: int, service: ShopMenuService = Depends(get_shop_menu_service)
):
    return await service.get_shop_menu(shop_id)

# Sorted by price asc
@router_public.get("/{shop_id}/sorted-price-asc", response_model=List[ShopMenuReadCustomer])
async def get_shop_menu(
    shop_id: int, service: ShopMenuService = Depends(get_shop_menu_service)
):
    return await service.get_shop_menu_sorted(shop_id, sort_by="price")

# Sorted by price desc
@router_public.get("/{shop_id}/sorted-price-desc", response_model=List[ShopMenuReadCustomer])
async def get_shop_menu(
    shop_id: int, service: ShopMenuService = Depends(get_shop_menu_service)
):
    return await service.get_shop_menu_sorted(shop_id, sort_by="price", order='desc')


# Sorted by name alphabet asc
@router_public.get("/{shop_id}/sorted-name-asc", response_model=List[ShopMenuReadCustomer])
async def get_shop_menu(
    shop_id: int, service: ShopMenuService = Depends(get_shop_menu_service)
):
    return await service.get_shop_menu_sorted(shop_id, sort_by="name", order='asc')






# -----------------------------
# MANAGER ENDPOINTS
# -----------------------------
router_manager = APIRouter(prefix="/manager/menu", tags=["Shop menu - Manager"])


@router_manager.post(
    "/", response_model=ShopMenuReadManagerAdmin, status_code=status.HTTP_201_CREATED
)
async def create_menu_item_manager(
    menu_in: ShopMenuCreateManager,
    current_user: User = Depends(require_manager_or_admin),
    service: ShopMenuService = Depends(get_shop_menu_service),
):
    try:
        item = await service.create_menu_item_manager(current_user.user_id, menu_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return item


# Update menu item
@router_manager.put("/{menu_id}", response_model=ShopMenuReadManagerAdmin)
async def update_menu_item_manager(
    menu_id: int,
    menu_in: ShopMenuUpdateManager,
    current_user: User = Depends(require_manager_or_admin),
    service: ShopMenuService = Depends(get_shop_menu_service),
):
    item = await service.get_menu_item_by_id(menu_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    updated = await service.update_menu_item_manager(
        current_user, item, menu_in.dict(exclude_unset=True)
    )
    return updated


@router_manager.get("/", response_model=List[ShopMenuReadManagerAdmin])
async def get_my_shop_menu_items(
    current_user: User = Depends(require_manager_or_admin),
    service: ShopMenuService = Depends(get_shop_menu_service),
):
    menu_items = await service.get_menu_for_manager(current_user.user_id)
    return menu_items


@router_manager.delete(
    "/{menu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_menu_item(
    menu_id: int,
    current_user: User = Depends(require_manager),
    service: ShopMenuService = Depends(get_shop_menu_service),
):
    item = await service.get_menu_item_by_id(menu_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    await service.delete_menu_item(item)


# -----------------------------
# ADMIN ENDPOINTS
# -----------------------------
router_admin = APIRouter(prefix="/admin/menu", tags=["Shop menu - Admin"])


# List all menu items
@router_admin.get("/", response_model=List[ShopMenuReadManagerAdmin])
async def list_all_menu_items(
    current_user: User = Depends(require_admin),
    service: ShopMenuService = Depends(get_shop_menu_service),
):
    return await service.get_all_menu_items()


# Create new item
@router_admin.post(
    "/",
    response_model=ShopMenuReadManagerAdmin,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu_item(
    menu_in: ShopMenuCreateAdmin,
    current_user: User = Depends(require_admin),
    service: ShopMenuService = Depends(get_shop_menu_service),
):
    try:
        item = await service.create_menu_item(menu_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return item


@router_admin.put(
    "/{menu_id}",
    response_model=ShopMenuReadManagerAdmin,
)
async def update_menu_item_admin(
    menu_id: int,
    menu_in: ShopMenuUpdateAdmin,
    current_user: User = Depends(require_admin),
    service: ShopMenuService = Depends(get_shop_menu_service),
):
    item = await service.get_menu_item_by_id(menu_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    updated = await service.update_menu_item_admin(
        item, menu_in.dict(exclude_unset=True)
    )
    return updated


# Delete menu item
@router_admin.delete(
    "/{menu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_menu_item(
    menu_id: int,
    current_user: User = Depends(require_admin),
    service: ShopMenuService = Depends(get_shop_menu_service),
):
    item = await service.get_menu_item_by_id(menu_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    await service.delete_menu_item(item)
