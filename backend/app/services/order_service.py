from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from datetime import datetime, date
from typing import Optional
from sqlalchemy.orm import selectinload, joinedload
from app.models import (
    Order,
    OrderItem,
    Product,
    User,
    CoffeeShop,
    ShopMenu,
    ProductAttributeOptions,
    ProductAttributes,
    OrderItemAttribute,
)
from app.schemas.orders_schema import OrderCreateCustomer


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, user_id: int, order_in: OrderCreateCustomer) -> Order:
        try:
            total_amount = 0
            order_items_specs = []

            for item_in in order_in.items:

                product = await self.db.get(Product, item_in.product_id)
                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product {item_in.product_id} not found",
                    )

                stmt = select(ShopMenu).where(
                    ShopMenu.shop_id == order_in.shop_id,
                    ShopMenu.product_id == item_in.product_id,
                    ShopMenu.is_available == True,
                )
                res = await self.db.execute(stmt)
                if not res.scalar_one_or_none():
                    raise HTTPException(
                        status_code=400,
                        detail=f"Product {item_in.product_id} is not available in shop {order_in.shop_id}",
                    )

                option_ids = list(dict.fromkeys(item_in.option_ids or []))  # unique
                options = []
                if option_ids:
                    q = (
                        select(ProductAttributeOptions)
                        .join(
                            ProductAttributes,
                            ProductAttributes.option_id
                            == ProductAttributeOptions.option_id,
                        )
                        .where(
                            ProductAttributes.product_id == item_in.product_id,
                            ProductAttributeOptions.option_id.in_(option_ids),
                        )
                    )
                    r = await self.db.execute(q)
                    options = r.scalars().all()
                    if len(options) != len(option_ids):
                        raise HTTPException(
                            status_code=400,
                            detail="Some selected attribute options are invalid for this product",
                        )

                    attr_type_ids = [o.attribute_type_id for o in options]
                    if len(attr_type_ids) != len(set(attr_type_ids)):
                        raise HTTPException(
                            status_code=400,
                            detail="Multiple options selected from the same attribute type",
                        )

                extra_sum = sum(o.extra_price for o in options)
                unit_price = product.price + extra_sum
                if unit_price < 0:
                    raise HTTPException(
                        status_code=400, detail="Computed unit_price is invalid"
                    )

                order_item = OrderItem(
                    product_id=item_in.product_id,
                    unit_price=unit_price,
                    quantity=item_in.quantity,
                )
                order_items_specs.append((order_item, [o.option_id for o in options]))

                total_amount += unit_price * item_in.quantity

            if total_amount < 0:
                raise HTTPException(
                    status_code=400, detail="Total amount cannot be negative"
                )

            order = Order(
                user_id=user_id,
                shop_id=order_in.shop_id,
                total_amount=total_amount,
                items=[spec[0] for spec in order_items_specs],
            )
            self.db.add(order)

            await self.db.flush()

            for oi, option_ids in order_items_specs:
                for opt_id in option_ids:
                    self.db.add(
                        OrderItemAttribute(
                            order_item_id=oi.order_item_id, option_id=opt_id
                        )
                    )

            await self.db.commit()

            query = select(Order).where(Order.order_id == order.order_id)
            load_opts = (
                selectinload(Order.items)
                .selectinload(OrderItem.attributes)
                .selectinload(OrderItemAttribute.option)
                .selectinload(ProductAttributeOptions.attribute_type)
            )
            res = await self.db.execute(query.options(load_opts))
            created = res.scalar_one()
            return created
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception:
            await self.db.rollback()
            raise HTTPException(
                status_code=500, detail="An error occurred while creating the order"
            )

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
        load_opts = (
            selectinload(Order.items)
            .selectinload(OrderItem.attributes)
            .selectinload(OrderItemAttribute.option)
            .selectinload(ProductAttributeOptions.attribute_type)
        )
        result = await self.db.execute(
            query.options(load_opts).order_by(Order.created_at.desc())
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
        load_opts = (
            selectinload(Order.items)
            .selectinload(OrderItem.attributes)
            .selectinload(OrderItemAttribute.option)
            .selectinload(ProductAttributeOptions.attribute_type)
        )
        result = await self.db.execute(
            query.options(load_opts).order_by(Order.created_at.desc())
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
        load_opts = (
            selectinload(Order.items)
            .selectinload(OrderItem.attributes)
            .selectinload(OrderItemAttribute.option)
            .selectinload(ProductAttributeOptions.attribute_type)
        )
        result = await self.db.execute(
            query.options(load_opts).order_by(Order.created_at.desc())
        )
        return result.scalars().all()

    async def get_order_for_user(self, user_id: int, order_id: int) -> Order:
        query = select(Order).where(
            Order.order_id == order_id, Order.user_id == user_id
        )
        load_opts = (
            selectinload(Order.items)
            .selectinload(OrderItem.attributes)
            .selectinload(OrderItemAttribute.option)
            .selectinload(ProductAttributeOptions.attribute_type)
        )
        res = await self.db.execute(query.options(load_opts))
        order = res.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    async def ensure_user_exists(self, user_id: int):
        u = await self.db.get(User, user_id)
        if not u:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return u

    async def ensure_manager_manages_shop(self, manager_user_id: int, shop_id: int):
        q = select(CoffeeShop).where(
            CoffeeShop.shop_id == shop_id, CoffeeShop.manager_id == manager_user_id
        )
        res = await self.db.execute(q)
        shop = res.scalar_one_or_none()
        if not shop:
            raise HTTPException(status_code=403, detail="You don't manage this shop")
        return shop

    async def get_order_for_manager_shop(self, user_id: int, order_id: int) -> Order:
        query = (
            select(Order)
            .join(CoffeeShop, Order.shop_id == CoffeeShop.shop_id)
            .where(CoffeeShop.manager_id == user_id, Order.order_id == order_id)
        )
        load_opts = (
            selectinload(Order.items)
            .selectinload(OrderItem.attributes)
            .selectinload(OrderItemAttribute.option)
            .selectinload(ProductAttributeOptions.attribute_type)
        )
        res = await self.db.execute(query.options(load_opts))
        order = res.scalar_one_or_none()
        if not order:
            raise HTTPException(
                status_code=404, detail="Order not found or not accessible"
            )
        return order

    async def get_order_admin(self, order_id: int) -> Order:
        query = select(Order).where(Order.order_id == order_id)
        load_opts = (
            selectinload(Order.items)
            .selectinload(OrderItem.attributes)
            .selectinload(OrderItemAttribute.option)
            .selectinload(ProductAttributeOptions.attribute_type)
        )
        res = await self.db.execute(query.options(load_opts))
        order = res.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    async def delete_order_admin(self, order_id: int):
        try:
            order = await self.get_order_admin(order_id)
            await self.db.delete(order)
            await self.db.commit()
            return
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting order")
