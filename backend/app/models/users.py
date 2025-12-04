from __future__ import annotations 
from typing import List, Optional
from app.db.base import Base
from sqlalchemy import String, Text, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from .orders import Order
from .coffee_shops import CoffeeShop


class UserRole(str, enum.Enum):
    customer = "customer"
    manager = "manager"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(50))
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), default=UserRole.customer
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    managed_shop: Mapped[Optional["CoffeeShop"]] = relationship(
        back_populates="manager"
    )
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
