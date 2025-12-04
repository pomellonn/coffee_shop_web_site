from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from models import ProductType


class ProductBase(BaseModel):
    name: str = Field(..., max_length=128, example="Эспрессо")
    description: Optional[str] = Field(None, example="Крепкий и ароматный кофе")
    image_url: Optional[str] = Field(None, example="")
    volume: int = Field(..., gt=0, example=300)
    product_type: ProductType = Field(..., example=ProductType.coffee)
    price: int = Field(..., ge=0, example=250)

    model_config = ConfigDict(from_attributes=True)


# Create schema
class ProductCreateManagerAdmin(ProductBase):
    pass


# Read schema - Customer View
class ProductReadCustomer(ProductBase):
    pass

# Read schema - Manager/Admin View
class ProductReadManagerAdmin(ProductBase):
    product_id: int


# Update schema
class ProductUpdateAdmin(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    volume: Optional[int] = None
    product_type: Optional[ProductType] = None
    price: Optional[int] = None

