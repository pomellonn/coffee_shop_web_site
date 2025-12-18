from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.coffeeshop_service import CoffeeShopService
from app.services.shopmenu_service import ShopMenuService
from app.services.order_service import OrderService
from app.services.attribute_types_service import AttributeTypesService
from app.services.product_attribute_options_service import ProductAttributeOptionsService
from app.services.product_attributes_service import ProductAttributesService

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


async def get_attribute_types_service(
    db: AsyncSession = Depends(get_session),
)-> AttributeTypesService:
    return AttributeTypesService(db)


async def get_product_attribute_options_service(
    db: AsyncSession = Depends(get_session),
)-> ProductAttributeOptionsService:
    return ProductAttributeOptionsService(db)


async def get_product_attributes_service(
    db: AsyncSession = Depends(get_session),
)-> ProductAttributesService:
    return ProductAttributesService(db)


async def get_attribute_types_service(
    db: AsyncSession = Depends(get_session),
)-> AttributeTypesService:
    return AttributeTypesService(db)


async def get_product_attribute_options_service(
    db: AsyncSession = Depends(get_session),
)-> ProductAttributeOptionsService:
    return ProductAttributeOptionsService(db)


async def get_product_attributes_service(
    db: AsyncSession = Depends(get_session),
)-> ProductAttributesService:
    return ProductAttributesService(db)


async def get_order_service(
    db: AsyncSession = Depends(get_session),
) -> OrderService:
    return OrderService(db)