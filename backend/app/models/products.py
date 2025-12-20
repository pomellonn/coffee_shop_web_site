from __future__ import annotations 
from typing import List, Optional
from app.db.base import Base
from sqlalchemy import String, Text, Enum, CheckConstraint, Integer, Identity
from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
import enum
from sqlalchemy.ext.associationproxy import association_proxy



class ProductType(str, enum.Enum):
    coffee = "coffee"
    non_coffee = "non_coffee"
    bakery = "bakery"


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    product_type: Mapped[ProductType] = mapped_column(
        Enum(ProductType, name="product_type"), default=ProductType.coffee
    )
    price: Mapped[int]

    menu_entries: Mapped[List["ShopMenu"]] = relationship(back_populates="product")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")
    
    
    product_attributes: Mapped[List["ProductAttributes"]] = relationship(
        "ProductAttributes",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    
    attribute_options = association_proxy("product_attributes", "option")


    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_nonnegative"),
    )

    @validates("price")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be non-negative")
        return value
