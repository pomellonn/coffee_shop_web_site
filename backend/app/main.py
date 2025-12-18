from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import sync_engine
from typing import Annotated
from app.api.api_router import api_router
from app.core.security import get_current_user
from app.models import User
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin


from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(title="Coffee Shop API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:80",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# admin = Admin(app, sync_engine, authentication_backend=authentication_backend)

# admin.add_view(UserAdmin)
# admin.add_view(CoffeeShopAdmin)
# admin.add_view(ProductAdmin)
# admin.add_view(OrderAdmin)

# admin.add_view(AnalyticsOneShopView)
# admin.add_view(AnalyticsAllShopsView)
# admin.add_view(AnalyticsClientsView)



# api
app.include_router(api_router, prefix="/api/v1")

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
