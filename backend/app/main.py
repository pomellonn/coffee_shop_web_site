from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from typing import Annotated
from api.api_router import api_router
from dependencies.auth import get_current_user
app = FastAPI(title="Coffee Shop API", version="1.0.0")

app.include_router(api_router, prefix="/api/v1") 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UserDep = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=200)
async def root(user: UserDep):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"user": user}
