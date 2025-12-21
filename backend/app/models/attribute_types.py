from __future__ import annotations 
from typing import List
from app.db.base import Base
from sqlalchemy import String, Integer, Identity
from sqlalchemy.orm import relationship, Mapped, mapped_column
   
class AttributeType(Base):
    __tablename__ = "attribute_types"
    attribute_type_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True)
    attribute_name: Mapped[str] =  mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    
    options: Mapped[List["ProductAttributeOptions"]] = relationship(
        "ProductAttributeOptions",
        back_populates="attribute_type",
        cascade="all, delete-orphan"
    )