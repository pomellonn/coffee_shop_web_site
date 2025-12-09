from fastapi import APIRouter
from api.endpoints import users, auth

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
# api_router.include_router(coffee_shops.router)
# api_router.include_router(products.router)
