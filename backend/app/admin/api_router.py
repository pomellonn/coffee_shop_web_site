from fastapi import APIRouter, Depends
from app.core.security import require_admin
from .endpoints import shop_menu, analytics

admin_api_router = APIRouter(
    prefix="/admin", tags=["Admin"]
)


admin_api_router.include_router(shop_menu.router, prefix="/shop-menu", tags=["Shop Menu"])
#admin_api_router.include_router(users.router, prefix="/users", tags=["Users"])
#admin_api_router.include_router(analytics.router)