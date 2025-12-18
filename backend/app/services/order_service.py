from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from datetime import datetime, date
from typing import Optional
from sqlalchemy.orm import selectinload, joinedload
from app.models import Order, OrderItem, Product, User, CoffeeShop, ShopMenu
from app.schemas.orders_schema import OrderCreateCustomer


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # CUSTOMER METHODS
    async def create_order(self, user_id: int, order_in: OrderCreateCustomer) -> Order:
        total_amount = 0
        order_items_to_create = []

        try:
            for item_in in order_in.items:

                product = await self.db.get(Product, item_in.product_id)
                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product ID {item_in.product_id} not found",
                    )

                result = await self.db.execute(
                    select(ShopMenu).where(
                        ShopMenu.shop_id == order_in.shop_id,
                        ShopMenu.product_id == item_in.product_id,
                        ShopMenu.is_available == True,
                    )
                )
                shop_menu_item = result.scalar_one_or_none()
                if not shop_menu_item:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Product ID {item_in.product_id} is not available in shop {order_in.shop_id}",
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

            if total_amount < 0:
                raise HTTPException(
                    status_code=400, detail="Total amount cannot be negative"
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

        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=500, detail="An error occurred while creating the order"
            )

    # Get order ordered by date, also with optional date filtering
    async def get_my_orders(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Order]:
        query = select(Order).where(Order.user_id == user_id)
        if start_date:
            query = query.where(Order.created_at >= start_date)
        if end_date:
            query = query.where(Order.created_at <= end_date)
        result = await self.db.execute(
            query.options(selectinload(Order.items)).order_by(Order.created_at.desc())
        )
        return result.scalars().all()

    # MANAGER/ADMIN METHODS
    async def get_orders_for_manager_shop(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Order]:
        query = (
            select(Order)
            .join(CoffeeShop, Order.shop_id == CoffeeShop.shop_id)
            .where(CoffeeShop.manager_id == user_id)
        )
        if start_date:
            query = query.where(Order.created_at >= start_date)
        if end_date:
            query = query.where(Order.created_at <= end_date)
        result = await self.db.execute(
            query.options(selectinload(Order.items)).order_by(Order.created_at.desc())
        )
        return result.scalars().all()

 

    async def get_orders_count_for_manager_shop(
        self,
        user_id: int,
        target_date: Optional[date] = None,
    ) -> int:
        query = (
            select(func.count(Order.order_id))
            .join(CoffeeShop, Order.shop_id == CoffeeShop.shop_id)
            .where(CoffeeShop.manager_id == user_id)
        )

        if target_date:
            query = query.where(cast(Order.created_at, Date) == target_date)

        result = await self.db.execute(query)
        count = result.scalar_one()  # возвращает число
        return count

    async def get_all_orders(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Order]:
        query = select(Order)
        if start_date:
            query = query.where(Order.created_at >= start_date)
        if end_date:
            query = query.where(Order.created_at <= end_date)
        result = await self.db.execute(
            query.options(selectinload(Order.items)).order_by(Order.created_at.desc())
        )
        return result.scalars().all()
