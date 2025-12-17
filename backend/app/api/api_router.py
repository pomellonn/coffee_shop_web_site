from fastapi import APIRouter
from .endpoints import users, auth, products, coffee_shops, shop_menu, attribute_types, product_attribute_options

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(coffee_shops.router)
api_router.include_router(shop_menu.router)
api_router.include_router(attribute_types.router)
api_router.include_router(product_attribute_options.router)
