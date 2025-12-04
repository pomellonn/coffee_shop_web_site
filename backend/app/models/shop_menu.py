from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship


class ShopMenu(Base):
    __tablename__ = "shop_menu"

    shop_menu_id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(
        Integer,
        ForeignKey("coffee_shops.shop_id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(
        Integer,
        ForeignKey("products.product_id", ondelete="RESTRICT"),
        nullable=False,
    )
    is_available = Column(Boolean, nullable=False, default=True)

    shop = relationship("CoffeeShop", back_populates="menu_items")
    product = relationship("Product", back_populates="menu_entries")

    __table_args__ = (
        UniqueConstraint("shop_id", "product_id", name="uq_shop_product"),
    )
