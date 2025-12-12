from __future__ import annotations 
from typing import List, Optional
from db.base import Base
from sqlalchemy import String, Text, Enum, CheckConstraint
from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
import enum


class ProductType(str, enum.Enum):
    coffee = "coffee"
    non_coffee = "non_coffee"
    bakery = "bakery"


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    volume: Mapped[int]
    product_type: Mapped[ProductType] = mapped_column(
        Enum(ProductType, name="product_type"), default=ProductType.coffee
    )
    price: Mapped[int]

    menu_entries: Mapped[List["ShopMenu"]] = relationship(back_populates="product")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")

    __table_args__ = (
        CheckConstraint("volume > 0", name="check_volume_positive"),
        CheckConstraint("price >= 0", name="check_price_nonnegative"),
    )

    @validates("volume")
    def validate_volume(self, key, value):
        if value <= 0:
            raise ValueError("Volume must be greater than 0")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be non-negative")
        return value
