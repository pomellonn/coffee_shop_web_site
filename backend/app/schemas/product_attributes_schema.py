from pydantic import BaseModel,ConfigDict
from typing import List

class ProductAttributesBase(BaseModel):
    product_id: int
    option_id: int
    
class ProductAttributesCreate(ProductAttributesBase):
    pass


class ProductAttributesReadAdminManager(ProductAttributesBase):
    model_config = ConfigDict(from_attributes=True)


class ProductAttributesOptionReadUser(BaseModel):
    option_id: int
    value: str
    extra_price: int

    model_config = ConfigDict(from_attributes=True)
    
class ProductAttributeReadUser(BaseModel):
    attribute_type_id: int
    attribute_name: str
    options: List[ProductAttributesOptionReadUser]


# User: все атрибуты товара
class ProductAttributesReadUser(BaseModel):
    product_id: int
    attributes: List[ProductAttributeReadUser]


    
    