from __future__ import annotations 
from typing import List
from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class ProductAttributeOptions(Base):
    __tablename__ = "product_attribute_options"
    option_id: Mapped[int]=mapped_column(primary_key=True, index=True)
    attribute_type_id: Mapped[int] = mapped_column(
        ForeignKey("attribute_types.attribute_type_id", ondelete="CASCADE"),
        nullable=False
    )
    value: Mapped[str] = mapped_column(nullable=False)
    extra_price: Mapped[int]=mapped_column(default=0, nullable=False)
    
    attribute_type: Mapped["AttributeType"] = relationship(
        "AttributeType",
        back_populates="options"
    )
    
    product_attributes: Mapped[List["ProductAttributes"]] = relationship(
        "ProductAttributes",
        back_populates="option",
        cascade="all, delete-orphan"
    )