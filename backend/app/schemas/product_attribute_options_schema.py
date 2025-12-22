from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProductAttributeOptionsBase(BaseModel):
    attribute_type_id: int = Field(..., example=1)
    value: str = Field(..., example="Коровье")
    extra_price: int = Field(default=0, example=30)
    
class ProductAttributeOptionsCreate(ProductAttributeOptionsBase):
    pass

class ProductAttributeOptionsUpdate(BaseModel):
    value: Optional[str] = Field(None, example="Кокосовое")
    extra_price: Optional[int] = Field(None, example=30)

class ProductAttributeOptionsRead(ProductAttributeOptionsBase):
    option_id: int = Field(..., example=1)
    model_config = ConfigDict(from_attributes=True)