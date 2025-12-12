from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload 

from models import CoffeeShop
from schemas.coffeeshop_schema import CoffeeShopCreateAdmin, CoffeeShopUpdateAdmin


class CoffeeShopService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_shop_by_id(self, shop_id: int) -> Optional[CoffeeShop]:
        result = await self.db.execute(
            select(CoffeeShop)
            .where(CoffeeShop.shop_id == shop_id)
            .options(selectinload(CoffeeShop.manager))
        )
        return result.scalar_one_or_none()

    async def get_all_shops(self) -> List[CoffeeShop]:
        result = await self.db.execute(
            select(CoffeeShop).options(selectinload(CoffeeShop.manager))
        )
        return result.scalars().all()

    async def create_shop(self, shop_in: CoffeeShopCreateAdmin) -> CoffeeShop:
        shop = CoffeeShop(
            name=shop_in.name,
            address=shop_in.address,
            manager_id=shop_in.manager_id,
        )
        self.db.add(shop)
        await self.db.commit()
        await self.db.refresh(shop)
        return shop

    async def update_shop(self, shop: CoffeeShop, updates: dict) -> CoffeeShop:
        for field, value in updates.items():
            setattr(shop, field, value)

        self.db.add(shop)
        await self.db.commit()
        await self.db.refresh(shop)
        return shop

    async def delete_shop(self, shop: CoffeeShop):
        await self.db.delete(shop)
        await self.db.commit()
