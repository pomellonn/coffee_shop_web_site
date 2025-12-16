from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    quantity: int = Field(..., gt=0, example=2)
    model_config = ConfigDict(from_attributes=True)


# Create schema - Customer View
class OrderItemCreateCustomer(OrderItemBase):
    product_id: int = Field(..., example=1)


# Read schema - Customer View
class OrderItemReadCustomer(OrderItemBase):
    product_id: int = Field(..., example=1)
    order_id: int = Field(..., example=1)
    unit_price: int = Field(..., ge=0, example=250)


# Read schema - Manager/Admin View
class OrderItemReadManagerAdmin(OrderItemBase):
    order_item_id: int
    order_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    unit_price: int = Field(..., ge=0, example=250)
