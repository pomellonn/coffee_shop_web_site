from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class OrderBase(BaseModel):
    shop_id: int = Field(..., example=1)
    model_config = ConfigDict(from_attributes=True)


# Create schema - Customer View
class OrderCreateCustomer(OrderBase):
    pass


# Read schema - Customer View
class OrderReadCustomer(OrderBase):
    order_id: int
    created_at: datetime = Field(..., example="2024-10-05T14:48:00.000Z")


# Read schema - Manager/Admin View
class OrderReadManagerAdmin(OrderReadCustomer):
    user_id: int = Field(..., example=1)
