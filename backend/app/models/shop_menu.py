from __future__ import annotations 
from app.db.base import Base
from sqlalchemy import ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .coffee_shops import CoffeeShop
from .products import Product


class ShopMenu(Base):
    __tablename__ = "shop_menu"

    shop_menu_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    shop_id: Mapped[int] = mapped_column(
        ForeignKey("coffee_shops.shop_id", ondelete="CASCADE"),
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.product_id", ondelete="RESTRICT"),
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    shop: Mapped["CoffeeShop"] = relationship(back_populates="menu_items")
    product: Mapped["Product"] = relationship(back_populates="menu_entries")

    __table_args__ = (
        UniqueConstraint("shop_id", "product_id", name="uq_shop_product"),
    )
