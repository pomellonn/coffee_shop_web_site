from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from db.session import get_session
from models.users import User, UserRole
from schemas.user_schema import (
    UserCreate,
    UserCreateAdmin,
    UserReadCustomer,
    UserReadManagerAdmin,
    UserUpdateCustomer,
    UserUpdateAdmin,
    UserWithToken,
    Token,
)
from dependencies.services import get_user_service

from core.security import get_current_user, require_admin
from services.user_service import UserService
from core.security import create_access_token
from core.config import settings
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/users", tags=["users"])

# -------------------
# CUSTOMER ENDPOINTS
# -------------------


# Register new user
@router.post(
    "/register", response_model=UserWithToken, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_in: UserCreate, user_service: UserService = Depends(get_user_service)
):

    existing_user = await user_service.get_user_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    db_user = await user_service.create_user(user_in)

    access_token = create_access_token(
        data={
            "user_id": db_user.user_id,
            "sub": db_user.email,
            "role": db_user.role.value,
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return UserWithToken(
        user=UserReadCustomer.from_orm(db_user),
        token=Token(access_token=access_token, token_type="bearer"),
    )


# Get current user info
@router.get("/me", response_model=UserReadCustomer)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# Update current user
@router.put("/me", response_model=UserReadCustomer)
async def update_me(
    user_in: UserUpdateCustomer,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    updated_user = await user_service.update_user(
        current_user,
        user_in.dict(exclude_unset=True),
    )
    return updated_user


# -------------------
# ADMIN ENDPOINTS
# -------------------


# ADMIN: Create any type of user
@router.post(
    "/admin/create",
    response_model=UserReadManagerAdmin,
    status_code=status.HTTP_201_CREATED,
    tags=["admin", "users"],
)
async def admin_create_user(
    user_in: UserCreateAdmin,
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
):

    existing = await user_service.get_user_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = await user_service.create_user_admin(user_in)

    return UserReadManagerAdmin.from_orm(db_user)


# List all users
@router.get("/", response_model=List[UserReadManagerAdmin])
async def list_users(
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.get_all_users()
    return users


# Update  user
@router.put("/{user_id}", response_model=UserReadManagerAdmin)
async def update_user_admin(
    user_id: int,
    user_in: UserUpdateAdmin,
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = await user_service.update_user(
        user,
        user_in.dict(exclude_unset=True),
    )
    return updated


# Delete user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_service.delete_user(user)
    return
