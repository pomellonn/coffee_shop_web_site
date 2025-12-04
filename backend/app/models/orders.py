from app.db.base import Base
from sqlalchemy import Column, Integer, TIMESTAMP, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, validates


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False
    )
    shop_id = Column(
        Integer, ForeignKey("coffee_shops.shop_id", ondelete="RESTRICT"), nullable=False
    )
    total_amount = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="orders")
    shop = relationship("CoffeeShop")
    items = relationship(
        "OrderItems", back_populates="order", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="check_total_amount_nonnegative"),
    )

    @validates("total_amount")
    def validate_total_amount(self, key, value):
        if value < 0:
            raise ValueError("Total amount must be non-negative")
        return value
