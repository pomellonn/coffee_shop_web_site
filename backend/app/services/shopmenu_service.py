from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status


from models import ShopMenu, CoffeeShop, User, UserRole
from schemas.shopmenu_schema import (
    ShopMenuCreateAdmin,
    ShopMenuCreateManager,
)


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

        #  or joinedload при refresh
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
