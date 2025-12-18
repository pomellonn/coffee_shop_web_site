from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from .product_schema import ProductName, ProductReadManagerAdmin


class ShopMenuBase(BaseModel):
    shop_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    is_available: bool = Field(..., example=True)

    model_config = ConfigDict(from_attributes=True)


class ShopMenuReadCustomer(ShopMenuBase):
    product: Optional[ProductName] = None
    model_config = ConfigDict(from_attributes=True)


# Create schema - Admin View
class ShopMenuCreateAdmin(ShopMenuBase):
    model_config = ConfigDict(from_attributes=True)


# Create schema - Manager View
class ShopMenuCreateManager(BaseModel):
    product_id: int = Field(..., example=1)
    is_available: bool = Field(True, example=True)
    model_config = ConfigDict(from_attributes=True)


# Read schema - Manager/Admin View
class ShopMenuReadManagerAdmin(ShopMenuBase):
    shop_menu_id: int
    product: Optional[ProductReadManagerAdmin] = None
    model_config = ConfigDict(from_attributes=True)


# Update schema - Manager View
class ShopMenuUpdateManager(BaseModel):
    product_id: Optional[int] = None
    is_available: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)


# Update schema - Admin View
class ShopMenuUpdateAdmin(ShopMenuUpdateManager):
    shop_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
