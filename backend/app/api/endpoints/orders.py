from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import date
from models import User, UserRole
from core.security import get_current_user, require_manager, require_admin
from schemas.orders_schema import (
    OrderCreateCustomer,
    OrderReadCustomer,
    OrderReadManagerAdmin,
    OrdersCountResponse,
)
from services.order_service import OrderService
from dependencies.services import get_order_service


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


@router_manager.get("/today", response_model=List[OrderReadManagerAdmin])
async def get_orders_for_my_shop(
    current_user: User = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
):
    today = date.today
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
   
    if not target_date:
        target_date = date.today()

    count = await service.get_orders_count_for_manager_shop(
        user_id=current_user.user_id,
        target_date=target_date
    )
    return OrdersCountResponse(count=count)

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
