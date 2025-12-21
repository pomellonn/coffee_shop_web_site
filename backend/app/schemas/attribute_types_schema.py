from pydantic import BaseModel,ConfigDict, Field
from typing import Optional


class AttributeTypeBase(BaseModel):
    attribute_name: str = Field(..., min_length=1, max_length=50, example="milk")

#только админ 
class AttributeTypeCreateManagerAdmin(AttributeTypeBase):
    pass
#только админ
class AttributeTypeUpdateManagerAdmin(BaseModel):
    attribute_name: Optional[str] = Field(None, min_length=1, max_length=50, example="size")
    class Config:
        from_attributes = True
    
# к read-get имеют доступ все пользователи 
class AttributeTypeRead(AttributeTypeBase):
    attribute_type_id: int = Field(..., example=1)
    model_config = ConfigDict(from_attributes=True)
