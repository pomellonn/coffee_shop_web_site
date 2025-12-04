from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, validates


class OrderItems(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(
        Integer,
        ForeignKey("products.product_id", ondelete="RESTRICT"),
        nullable=False,
    )
    unit_price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

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
