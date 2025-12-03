from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Text,
    Enum,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship, declarative_base
from database import Base
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    customer = "customer"
    manager = "manager"
    admin = "admin"


Base = declarative_base()


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


class CoffeeShop(Base):
    __tablename__ = "coffee_shops"

    shop_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    address = Column(String(256), nullable=False)
    manager_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
