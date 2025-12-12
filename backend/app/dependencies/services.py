from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from services.user_service import UserService
from services.product_service import ProductService
from services.coffeeshop_service import CoffeeShopService
from services.shopmenu_service import ShopMenuService

async def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(db)


async def get_product_service(
    db: AsyncSession = Depends(get_session),
) -> ProductService:
    return ProductService(db)


async def get_coffee_shop_service(
    db: AsyncSession = Depends(get_session),
) -> CoffeeShopService:
    return CoffeeShopService(db)


async def get_shop_menu_service(
    db: AsyncSession = Depends(get_session),
) -> ShopMenuService:
    return ShopMenuService(db)
