from __future__ import annotations
from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class OrderItemAttribute(Base):
    __tablename__ = "order_item_attributes"

    order_item_id: Mapped[int] = mapped_column(
        ForeignKey("order_items.order_item_id", ondelete="CASCADE"),
        primary_key=True,
    )
    option_id: Mapped[int] = mapped_column(
        ForeignKey("product_attribute_options.option_id", ondelete="CASCADE"),
        primary_key=True,
    )

    option: Mapped["ProductAttributeOptions"] = relationship("ProductAttributeOptions")
    order_item: Mapped["OrderItem"] = relationship(
        "OrderItem", back_populates="attributes"
    )