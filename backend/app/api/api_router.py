from fastapi import APIRouter
from .endpoints import orders, users, auth, products, coffee_shops, shop_menu, analytics, attribute_types, product_attribute_options, product_attributes

api_router = APIRouter()
api_router.include_router(auth.router)


# Public routes
api_router.include_router(users.router_public)
api_router.include_router(products.router_public)
api_router.include_router(coffee_shops.router_public)
api_router.include_router(shop_menu.router_public)
api_router.include_router(orders.router_public)

# Admin routes
api_router.include_router(users.router_admin)
api_router.include_router(products.router_admin)
api_router.include_router(coffee_shops.router_admin)
api_router.include_router(shop_menu.router_admin)
api_router.include_router(analytics.router_admin)
api_router.include_router(orders.router_admin)

# Manager routes
api_router.include_router(coffee_shops.router_manager)
api_router.include_router(shop_menu.router_manager)
api_router.include_router(analytics.router_manager)
api_router.include_router(orders.router_manager)
api_router.include_router(attribute_types.router)
api_router.include_router(product_attribute_options.router)
api_router.include_router(product_attributes.router)
