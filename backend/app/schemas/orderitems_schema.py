from pydantic import BaseModel, ConfigDict, Field
from typing import List


class OrderItemBase(BaseModel):
    quantity: int = Field(..., gt=0, example=2)
    model_config = ConfigDict(from_attributes=True)


# Create schema - Customer View
class OrderItemCreateCustomer(OrderItemBase):
    product_id: int = Field(..., example=1)
    option_ids: List[int] = Field(default_factory=list, example=[2, 5])


class SelectedOption(BaseModel):
    option_id: int
    attribute_type: str
    value: str
    extra_price: int


# Read schema - Customer View
class OrderItemReadCustomer(OrderItemBase):
    order_item_id: int
    product_id: int = Field(..., example=1)
    unit_price: int
    quantity: int
    selected_options: List[SelectedOption] = []


# Read schema - Manager/Admin View
class OrderItemReadManagerAdmin(OrderItemBase):
    order_item_id: int
    order_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    unit_price: int = Field(..., ge=0, example=250)
    selected_options: List[SelectedOption] = []
