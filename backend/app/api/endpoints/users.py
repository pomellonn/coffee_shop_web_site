from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from db.session import get_session
from models.users import User, UserRole
from schemas.user_schema import (
    UserCreate,
    UserReadCustomer,
    UserReadManagerAdmin,
    UserUpdateCustomer,
    UserUpdateAdmin,
    UserWithToken,
    Token,
)

from core.security import get_password_hash, verify_password
from dependencies.auth import get_current_user
from sqlalchemy.orm import Session
from core.security import create_access_token
from datetime import timedelta
from core.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/users", tags=["users"])


# Register new user - customer role by default
@router.post("/register", response_model=UserWithToken)
async def register_user(user_in: UserCreate, db: Session = Depends(get_session)):
    # Check if email already exists
    result = await db.execute(select(User).filter(User.email == user_in.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    db_user = User(
        email=user_in.email,
        name=user_in.name,
        password_hash=get_password_hash(user_in.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Create token
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return UserWithToken(
        user=UserReadCustomer.from_orm(db_user), token=Token(access_token=access_token)
    )


# Info about all users - admin only
@router.get("/", response_model=List[UserReadManagerAdmin])
async def list_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Access denied")
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/me", response_model=UserReadCustomer)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


# Update user
@router.put("/me", response_model=UserReadCustomer)
async def update_my_info(
    user_in: UserUpdateCustomer,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


# Update user by admin
@router.put("/{user_id}", response_model=UserUpdateAdmin)
async def update_user_admin(
    user_id: int,
    user_in: UserUpdateAdmin,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Access denied")
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_in.dict(exclude_unset=True).items():
        if field == "password":
            setattr(user, "password_hash", get_password_hash(value))
        else:
            setattr(user, field, value)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# Delete user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Access denied")
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return
