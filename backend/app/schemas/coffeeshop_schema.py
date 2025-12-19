from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from .user_schema import ManagerName

class CoffeeShopBase(BaseModel):
    name: str = Field(..., max_length=128, example="FLTR - Nevsky")
    address: str = Field(
        ..., max_length=256, example="Санкт-Петербург, Невский проспект, 28"
    )

    model_config = ConfigDict(from_attributes=True)


# Create schema - Admin View
class CoffeeShopCreateAdmin(CoffeeShopBase):
    manager_id: Optional[int] = Field(None, example=1) 
    model_config = ConfigDict(from_attributes=True)


# Read schema - Customer View
class CoffeeShopReadCustomer(CoffeeShopBase):
    shop_id: int
    model_config = ConfigDict(from_attributes=True)


# Read schema - Manager/Admin View
class CoffeeShopReadManagerAdmin(CoffeeShopBase):
    shop_id: int
    manager_id: Optional[int] = Field(None, example=1)
    manager: Optional[ManagerName] = None 
    model_config = ConfigDict(from_attributes=True)


# Update schema - Admin View
class CoffeeShopUpdateAdmin(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    manager_id: Optional[int] = None 
    
    model_config = ConfigDict(from_attributes=True)

