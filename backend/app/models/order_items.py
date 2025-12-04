from __future__ import annotations 
from typing import Optional
from app.db.base import Base
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from .orders import Order
from .products import Product

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.order_id", ondelete="CASCADE")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.product_id", ondelete="RESTRICT")
    )
    unit_price: Mapped[int]
    quantity: Mapped[int]

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")

    __table_args__ = (
        CheckConstraint("unit_price >= 0", name="check_unit_price_positive"),
        CheckConstraint("quantity >= 1", name="check_quantity_positive"),
    )

    @validates("unit_price")
    def validate_unit_price(self, key, value):
        if value < 0:
            raise ValueError("Unit price must be non-negative")
        return value

    @validates("quantity")
    def validate_quantity(self, key, value):
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        return value
