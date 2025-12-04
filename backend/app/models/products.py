from app.db.base import Base
from sqlalchemy import Column, Integer, String, Enum, Text, CheckConstraint
from sqlalchemy.orm import relationship, validates

import enum


class ProductType(str, enum.Enum):
    coffee = "coffee"
    non_coffee = "non_coffee"
    bakery = "bakery"


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    volume = Column(Integer, nullable=False)
    product_type = Column(
        Enum(ProductType, name="product_type"), nullable=False, default=ProductType.coffee
    )
    price = Column(Integer, nullable=False)

    menu_entries = relationship("ShopMenu", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

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
