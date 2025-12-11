from fastapi import APIRouter
from .endpoints import users, auth, products, coffee_shops

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(coffee_shops.router)

