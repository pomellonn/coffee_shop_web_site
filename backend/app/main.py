from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from db.session import sync_engine
from typing import Annotated
from api.api_router import api_router
from core.security import get_current_user
from models import User
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from admin.admin import (
    UserAdmin,
    CoffeeShopAdmin,
    ProductAdmin,
    OrderAdmin,
    AnalyticsAllShopsView,
    AnalyticsClientsView,
    AnalyticsOneShopView,
)
from admin.api_router import admin_api_router
from admin.authentication import authentication_backend, SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(title="Coffee Shop API", version="1.0.0")


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, https_only=True)

admin = Admin(app, sync_engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(CoffeeShopAdmin)
admin.add_view(ProductAdmin)
admin.add_view(OrderAdmin)

admin.add_view(AnalyticsOneShopView)
admin.add_view(AnalyticsAllShopsView)
admin.add_view(AnalyticsClientsView)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

# customer api
app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UserDep = Annotated[User, Depends(get_current_user)]


@app.get("/", status_code=200)
async def root(user: UserDep):
    return {
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value,
            "created_at": user.created_at,
        }
    }
