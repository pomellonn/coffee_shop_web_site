from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from services.user_service import UserService
from services.product_service import ProductService

async def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(db)

async def get_product_service(db: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(db)
