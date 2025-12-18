from __future__ import annotations 
from typing import List
from app.db.base import Base
from sqlalchemy import ForeignKey, CheckConstraint, func, TIMESTAMP
from sqlalchemy.orm import relationship, validates, Mapped, mapped_column


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT")
    )
    shop_id: Mapped[int] = mapped_column(
        ForeignKey("coffee_shops.shop_id", ondelete="RESTRICT")
    )
    total_amount: Mapped[int]
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="orders")
    shop: Mapped["CoffeeShop"] = relationship()
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="check_total_amount_nonnegative"),
    )

    @validates("total_amount")
    def validate_total_amount(self, key, value):
        if value < 0:
            raise ValueError("Total amount must be non-negative")
        return value
