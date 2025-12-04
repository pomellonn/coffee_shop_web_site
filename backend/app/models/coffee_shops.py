from app.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class CoffeeShop(Base):
    __tablename__ = "coffee_shops"

    shop_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    address = Column(String(256), nullable=False)
    manager_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )

    manager = relationship("User", back_populates="managed_shop")
    menu_items = relationship(
        "ShopMenu", back_populates="shop", cascade="all, delete-orphan"
    )
