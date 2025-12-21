from pydantic import BaseModel, ConfigDict, Field
from typing import List

class ProductAttributesBase(BaseModel):
    product_id: int = Field(..., example=1)
    option_id: int = Field(..., example=5)
    
class ProductAttributesCreate(ProductAttributesBase):
    pass


class ProductAttributesReadAdminManager(ProductAttributesBase):
    model_config = ConfigDict(from_attributes=True)


class ProductAttributesOptionReadUser(BaseModel):
    option_id: int = Field(..., example=5)
    value: str = Field(..., example="Безлактозное")
    extra_price: int = Field(..., example=30)

    model_config = ConfigDict(from_attributes=True)
    
class ProductAttributeReadUser(BaseModel):
    attribute_type_id: int = Field(..., example=1)
    attribute_name: str = Field(..., example="milk")
    options: List[ProductAttributesOptionReadUser]


# User: все атрибуты товара
class ProductAttributesReadUser(BaseModel):
    product_id: int = Field(..., example=1)
    attributes: List[ProductAttributeReadUser]


    
    