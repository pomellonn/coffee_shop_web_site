from pydantic import BaseModel,ConfigDict, Field
from typing import Optional
# from models import ProductAttributeOptions

class ProductAttributeOptionsBase(BaseModel):
    attribute_type_id:int
    value: str
    extra_price: int = 0
    
class ProductAttributeOptionsCreate(ProductAttributeOptionsBase):
    pass

class ProductAttributeOptionsUpdate(BaseModel):
    value: Optional[str] = None
    extra_price: Optional[int] = None

class ProductAttributeOptionsRead(ProductAttributeOptionsBase):
    option_id: int
    model_config = ConfigDict(from_attributes=True)