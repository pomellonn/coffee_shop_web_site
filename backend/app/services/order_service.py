# app/services/order_service.py

from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from models import Order, OrderItem, Product, User, CoffeeShop
from schemas.orders_schema import OrderCreateCustomer


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # CUSTOMER METHODS
    async def create_order(self, user_id: int, order_in: OrderCreateCustomer) -> Order:

        order_items_to_create = []

        for item_in in order_in.items:

            product = await self.db.get(Product, item_in.product_id)
            if not product:
                raise HTTPException(
                    status_code=404, detail=f"Product ID {item_in.product_id} not found"
                )

            unit_price = product.price
            total_amount += unit_price * item_in.quantity

            order_items_to_create.append(
                OrderItem(
                    product_id=item_in.product_id,
                    unit_price=unit_price,
                    quantity=item_in.quantity,
                )
            )

        order = Order(
            user_id=user_id,
            shop_id=order_in.shop_id,
            total_amount=total_amount,
            items=order_items_to_create,
        )

        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order, attribute_names=["items"])
        return order

    async def get_my_orders(self, user_id: int) -> List[Order]:

        result = await self.db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()

    # MANAGER/ADMIN METHODS
    async def get_orders_for_manager_shop(self, user_id: int) -> List[Order]:

        result = await self.db.execute(
            select(Order)
            .join(CoffeeShop, Order.shop_id == CoffeeShop.shop_id)
            .where(CoffeeShop.manager_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()

    async def get_all_orders(self) -> List[Order]:

        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()
