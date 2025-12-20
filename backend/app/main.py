from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from app.api.api_router import api_router
from app.core.security import get_current_user
from app.models import User
from fastapi.staticfiles import StaticFiles
from pathlib import Path

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

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
