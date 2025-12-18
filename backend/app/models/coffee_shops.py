from __future__ import annotations 
from app.db.base import Base
from typing import Optional, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


class CoffeeShop(Base):
    __tablename__ = "coffee_shops"

    shop_id: Mapped[int] = mapped_column(primary_key=True, index=True) 
    name: Mapped[str] = mapped_column(String(128)) 
    address: Mapped[str] = mapped_column(String(256))
    manager_id: Mapped[Optional[int]] = mapped_column( 
        ForeignKey("users.user_id", ondelete="SET NULL"),
        unique=True,
    )

    manager: Mapped[Optional["User"]] = relationship(back_populates="managed_shop")
    menu_items: Mapped[List["ShopMenu"]] = relationship(
        back_populates="shop", 
        cascade="all, delete-orphan"
    )

