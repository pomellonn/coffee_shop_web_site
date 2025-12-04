from app.db.base import Base
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, Text, func
from sqlalchemy.orm import relationship
import enum


class UserRole(str, enum.Enum):
    customer = "customer"
    manager = "manager"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    name = Column(String(50), nullable=False)
    role = Column(
        Enum(UserRole, name="user_role"), nullable=False, default=UserRole.customer
    )
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    managed_shop = relationship("CoffeeShop", back_populates="manager")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
