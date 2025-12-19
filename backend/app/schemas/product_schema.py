from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.models import ProductType


class ProductBase(BaseModel):
    name: str = Field(..., max_length=128, example="Эспрессо")
    description: Optional[str] = Field(None, example="Крепкий и ароматный кофе")
    image_url: Optional[str] = Field(None, example="")
    product_type: ProductType = Field(..., example=ProductType.coffee)
    price: int = Field(..., ge=0, example=250)

    model_config = ConfigDict(from_attributes=True)


# Create schema
class ProductCreateManagerAdmin(ProductBase):
    model_config = ConfigDict(from_attributes=True)


# Read schema - Customer View
class ProductReadCustomer(ProductBase):
    product_id: int
    model_config = ConfigDict(from_attributes=True)

# Read schema - Manager/Admin View
class ProductReadManagerAdmin(ProductBase):
    product_id: int
    model_config = ConfigDict(from_attributes=True)


# Update schema
class ProductUpdateAdmin(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    product_type: Optional[ProductType] = None
    price: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class ProductName(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    product_type: ProductType
    price: int
    model_config = ConfigDict(from_attributes=True)