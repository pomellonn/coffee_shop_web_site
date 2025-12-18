from __future__ import annotations 
from db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class ProductAttributes(Base):
    __tablename__ = "product_attributes"
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.product_id", ondelete="CASCADE"),
        primary_key=True,
    )
    option_id: Mapped[int]=mapped_column(
        ForeignKey("product_attribute_options.option_id", ondelete="CASCADE"),
       primary_key=True,
    )
    
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="product_attributes"
    )
    
    option: Mapped["ProductAttributeOptions"] = relationship(
        "ProductAttributeOptions",
        back_populates="product_attributes",
    )
    