from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users import User, UserRole
from app.schemas.user_schema import UserCreate, UserUpdateAdmin, UserCreateAdmin
from app.core.security import get_password_hash


class UserService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # GET USER METHODS
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.db.get(User, user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    # CREATE USER: CUSTOMER
    async def create_user(self, user_in: UserCreate) -> User:

        hashed_password = get_password_hash(user_in.password)

        db_user = User(
            email=user_in.email,
            name=user_in.name,
            password_hash=hashed_password,
            role=UserRole.customer,
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    # CREATE USER: ADMIN
    async def create_user_admin(self, user_in: UserCreateAdmin) -> User:
        hashed_password = get_password_hash(user_in.password)

        db_user = User(
            email=user_in.email,
            name=user_in.name,
            password_hash=hashed_password,
            role=user_in.role,
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    # UPDATE USER (Admin / Self)
    async def update_user(self, user: User, updates: dict) -> User:
        for field, value in updates.items():
            if field == "password":
                setattr(user, "password_hash", get_password_hash(value))
            else:
                setattr(user, field, value)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # DELETE USER
    async def delete_user(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()
        return

