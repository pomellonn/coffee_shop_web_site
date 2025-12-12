from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from typing import Annotated
from api.api_router import api_router
from core.security import get_current_user
from models import User

app = FastAPI(title="Coffee Shop API", version="1.0.0")

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
