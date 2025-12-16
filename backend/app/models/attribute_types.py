from __future__ import annotations 
from typing import List
from db.base import Base
import enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

class AttributeName(str, enum.Enum):
    milk="milk"
    syrup="syrup"
    roast="roast"
    size="size"
    
class AttributeType(Base):
    __tablename__ = "attribute_types"
    attribute_type_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    attribute_name: Mapped[AttributeName] =  mapped_column(
        SQLEnum(AttributeName, name="attribute_name"),
        nullable=False,
        unique=True
    )
    
    options: Mapped[List["ProductAttributeOptions"]] = relationship(
        "ProductAttributeOptions",
        back_populates="attribute_type",
        cascade="all, delete-orphan"
    )
    
    @property
    def display_name(self) -> str:
        mapping = {
            AttributeName.milk: "Тип молока",
            AttributeName.size: "Размер",
            AttributeName.syrup: "Тип сиропа",
            AttributeName.roast: "Обжарка",
        }
        return mapping[self.attribute_name]

   