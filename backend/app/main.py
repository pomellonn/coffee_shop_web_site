from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router, get_current_user
from database import engine
from typing import Annotated

app = FastAPI(title="Coffee Shop API", version="1.0.0")

app.include_router(auth_router)


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
