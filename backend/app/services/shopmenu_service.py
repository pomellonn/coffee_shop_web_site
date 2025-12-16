from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from models import Product
from models import ShopMenu, CoffeeShop, User, UserRole, OrderItem, Order
from schemas.shopmenu_schema import (
    ShopMenuCreateAdmin,
    ShopMenuCreateManager,
)
from sqlalchemy import func


class ShopMenuService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_menu_item_by_id(self, menu_id: int) -> Optional[ShopMenu]:
        return await self.db.get(ShopMenu, menu_id)

    async def get_all_menu_items(self) -> List[ShopMenu]:
        result = await self.db.execute(
            select(ShopMenu).options(selectinload(ShopMenu.product))
        )
        return result.scalars().all()

    async def get_shop_menu(self, shop_id: int) -> List[ShopMenu]:
        result = await self.db.execute(
            select(ShopMenu)
            .where(ShopMenu.shop_id == shop_id)
            .options(selectinload(ShopMenu.product))
        )
        return result.scalars().all()

    async def create_menu_item(self, item_in: ShopMenuCreateAdmin) -> ShopMenu:

        item = ShopMenu(
            shop_id=item_in.shop_id,
            product_id=item_in.product_id,
            is_available=item_in.is_available,
        )
        self.db.add(item)

        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("This product is already in the shop menu")

        await self.db.refresh(item)
        return item

    # Sort menu items by price or name
    async def get_shop_menu_sorted(
        self, shop_id: int, sort_by: str = "price", order: str = "asc"
    ) -> List[ShopMenu]:

        allowed_sort_fields = {"price", "name"}
        if sort_by not in allowed_sort_fields:
            sort_by = "price"

        sort_order = asc if order.lower() == "asc" else desc

        query = (
            select(ShopMenu)
            .where(ShopMenu.shop_id == shop_id)
            .options(selectinload(ShopMenu.product))
        )
        query = query.join(Product)
        if sort_by == "price":
            query = query.order_by(sort_order(Product.price))
        elif sort_by == "name":
            query = query.order_by(sort_order(Product.name))

        result = await self.db.execute(query)
        return result.scalars().all()
# Sort menu items by popularity (most sold first)
    async def get_shop_menu_by_popularity(
        self, shop_id: int, limit: int = 100
    ) -> List[ShopMenu]:

        sales_count_cte = (
            select(
                OrderItem.product_id, func.sum(OrderItem.quantity).label("total_sold")
            )
            .join(Order)
            .where(Order.shop_id == shop_id)
            .group_by(OrderItem.product_id)
            .cte("sales_count")
        )

        query = select(ShopMenu).where(ShopMenu.shop_id == shop_id)

        query = query.join(
            sales_count_cte,
            ShopMenu.product_id == sales_count_cte.c.product_id,
            isouter=True,
        )

        query = query.order_by(desc(sales_count_cte.c.total_sold)).order_by(
            ShopMenu.product_id
        )

        query = query.options(selectinload(ShopMenu.product)).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_menu_item_admin(self, item: ShopMenu, updates: dict) -> ShopMenu:

        for field, value in updates.items():
            if value is not None:
                setattr(item, field, value)

        self.db.add(item)

        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("This updated menu conflicts with unique constraints")

        await self.db.refresh(item)
        return item

    async def get_menu_for_manager(self, user_id: int) -> List[ShopMenu]:

        result = await self.db.execute(
            select(ShopMenu)
            .join(CoffeeShop)
            .join(User, CoffeeShop.manager_id == User.user_id)
            .where(User.user_id == user_id)
            .options(selectinload(ShopMenu.product))
        )
        return result.scalars().all()

    async def create_menu_item_manager(
        self, user_id: int, item_in: ShopMenuCreateManager
    ) -> ShopMenu:
        result = await self.db.execute(
            select(CoffeeShop).where(CoffeeShop.manager_id == user_id)
        )
        shop = result.scalar_one_or_none()

        if not shop:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not assigned as a manager to any coffee shop",
            )

        shop_id = shop.shop_id

        item = ShopMenu(
            shop_id=shop_id,
            product_id=item_in.product_id,
            is_available=item_in.is_available,
        )
        self.db.add(item)

        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("This product is already in the shop menu")

        await self.db.refresh(item, attribute_names=["product"])
        return item

    async def update_menu_item_manager(
        self, user: User, item: ShopMenu, updates: dict
    ) -> ShopMenu:
        if user.role == UserRole.admin:
            allowed_fields = {"product_id", "is_available", "shop_id"}
        else:
            result = await self.db.execute(
                select(CoffeeShop).where(
                    CoffeeShop.shop_id == item.shop_id,
                    CoffeeShop.manager_id == user.user_id,
                )
            )
            shop = result.scalar_one_or_none()
            if not shop:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not allowed to modify this menu item",
                )
            allowed_fields = {"product_id", "is_available"}

        for field, value in updates.items():
            if field in allowed_fields and value is not None:
                setattr(item, field, value)

        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item, attribute_names=["product"])
        return item


    async def delete_menu_item(self, item: ShopMenu) -> None:
        await self.db.delete(item)
        await self.db.commit()
