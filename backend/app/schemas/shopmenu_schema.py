from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ShopMenuBase(BaseModel):
    shop_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    is_available: bool = Field(..., example=True)

    model_config = ConfigDict(from_attributes=True)


class ShopMenuReadCustomer(ShopMenuBase):
    pass


# Create schema - Admin View
class ShopMenuCreateAdmin(ShopMenuBase):
    pass


# Read schema - Manager/Admin View
class ShopMenuReadManagerAdmin(ShopMenuBase):
    shop_menu_id: int


# Update schema - Manager View
class ShopMenuUpdateManager(BaseModel):
    product_id: Optional[int] = None
    is_available: Optional[bool] = None


# Update schema - Admin View
class ShopMenuUpdateAdmin(ShopMenuUpdateManager):
    shop_id: Optional[int] = None
