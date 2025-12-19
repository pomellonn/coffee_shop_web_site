from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from .orderitems_schema import (
    OrderItemCreateCustomer,
    OrderItemReadCustomer,
    OrderItemReadManagerAdmin,
)
from typing import List, Optional


class OrderBase(BaseModel):
    shop_id: int = Field(..., example=1)
    model_config = ConfigDict(from_attributes=True)


# Create schema - Customer View
class OrderCreateCustomer(OrderBase):
    items: List[OrderItemCreateCustomer] = Field(..., min_items=1)


class OrderCreateByStaff(OrderBase):
    user_id: int = Field(..., example=1)
    items: List[OrderItemCreateCustomer] = Field(..., min_items=1)


# Read schema - Customer View
class OrderReadCustomer(OrderBase):
    order_id: int
    created_at: datetime
    items: List[OrderItemReadCustomer] = []
    total_amount: int
    
# Read schema - Manager/Admin View
class OrderReadManagerAdmin(OrderReadCustomer):
    user_id: int = Field(..., example=1)
    items: List[OrderItemReadManagerAdmin] = []
    total_amount: int = Field(..., ge=0, example=500)


class OrdersCountResponse(BaseModel):
    count: int
