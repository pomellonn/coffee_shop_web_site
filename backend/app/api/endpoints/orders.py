from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import date
from app.models import User, UserRole
from app.core.security import get_current_user, require_manager, require_admin
from app.schemas.orders_schema import (
    OrderCreateCustomer,
    OrderCreateByStaff,
    OrderReadCustomer,
    OrderReadManagerAdmin,
    OrdersCountResponse,
)
from app.services.order_service import OrderService
from app.dependencies.services import get_order_service


# -----------------------------
# CUSTOMER ENDPOINTS
# -----------------------------

router_public = APIRouter(prefix="/orders", tags=["Orders - Customer"])


@router_public.post(
    "/", response_model=OrderReadCustomer, status_code=status.HTTP_201_CREATED
)
async def create_order(
    order_in: OrderCreateCustomer,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):

    order = await service.create_order(current_user.user_id, order_in)
    return order


@router_public.get("/me", response_model=List[OrderReadCustomer])
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    orders = await service.get_my_orders(current_user.user_id)
    return orders


@router_public.get("/{order_id}", response_model=OrderReadCustomer)
async def get_my_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    order = await service.get_order_for_user(current_user.user_id, order_id)
    return order


# -----------------------------
# MANAGER ENDPOINTS
# -----------------------------

router_manager = APIRouter(prefix="/manager/orders", tags=["Orders - Manager"])


@router_manager.get("/", response_model=List[OrderReadManagerAdmin])
async def get_orders_for_my_shop(
    current_user: User = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
):
    orders = await service.get_orders_for_manager_shop(current_user.user_id)
    return orders


@router_manager.post("/", response_model=OrderReadManagerAdmin, status_code=status.HTTP_201_CREATED)
async def manager_create_order(
    order_in: OrderCreateByStaff,
    current_user: User = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
):

    await service.ensure_manager_manages_shop(current_user.user_id, order_in.shop_id)
    await service.ensure_user_exists(order_in.user_id)
    order_payload = OrderCreateCustomer(shop_id=order_in.shop_id, items=order_in.items)
    order = await service.create_order(order_in.user_id, order_payload)
    return order




@router_manager.get("/today", response_model=List[OrderReadManagerAdmin])
async def get_orders_for_my_shop(
    current_user: User = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
):
    today = date.today()
    orders = await service.get_orders_for_manager_shop(        
        user_id=current_user.user_id,
        start_date=today,
        end_date=today)
    return orders

@router_manager.get("/orders-count", response_model=OrdersCountResponse)
async def get_orders_count_for_my_shop(
    current_user: User = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
    target_date: Optional[date] = Query(None, description="Дата для подсчета заказов, формат YYYY-MM-DD")
):
    import logging
    logging.getLogger("uvicorn.error").debug("orders-count called; target_date=%s", target_date)

    if not target_date:
        target_date = date.today()

    count = await service.get_orders_count_for_manager_shop(
        user_id=current_user.user_id,
        target_date=target_date
    )
    return OrdersCountResponse(count=count)


@router_manager.get("/{order_id}", response_model=OrderReadManagerAdmin)
async def get_order_for_my_shop(
    order_id: int,
    current_user: User = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
):
    order = await service.get_order_for_manager_shop(current_user.user_id, order_id)
    return order

router_admin = APIRouter(prefix="/admin/orders", tags=["Orders - Admin"])



# -----------------------------
# ADMIN ENDPOINTS
# -----------------------------

@router_admin.get("/", response_model=List[OrderReadManagerAdmin])
async def list_all_orders_admin(
    current_user: User = Depends(require_admin),
    service: OrderService = Depends(get_order_service),
):

    orders = await service.get_all_orders()
    return orders


@router_admin.post("/", response_model=OrderReadManagerAdmin, status_code=status.HTTP_201_CREATED)
async def admin_create_order(
    order_in: OrderCreateByStaff,
    current_user: User = Depends(require_admin),
    service: OrderService = Depends(get_order_service),
):
    # ensure target user exists
    await service.ensure_user_exists(order_in.user_id)
    order_payload = OrderCreateCustomer(shop_id=order_in.shop_id, items=order_in.items)
    order = await service.create_order(order_in.user_id, order_payload)
    return order


@router_admin.get("/{order_id}", response_model=OrderReadManagerAdmin)
async def get_order_admin(
    order_id: int,
    current_user: User = Depends(require_admin),
    service: OrderService = Depends(get_order_service),
):
    order = await service.get_order_admin(order_id)
    return order


@router_admin.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_admin(
    order_id: int,
    current_user: User = Depends(require_admin),
    service: OrderService = Depends(get_order_service),
):
    await service.delete_order_admin(order_id)
    return None
