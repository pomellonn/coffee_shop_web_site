from pydantic import BaseModel,ConfigDict, Field
from typing import Optional
from models import AttributeName

class AttributeTypeBase(BaseModel):
    attribute_name: AttributeName= Field(..., example=AttributeName.milk)
    class Config:
        from_attributes = True

#только админ 
class AttributeTypeCreateManagerAdmin(AttributeTypeBase):
    pass
#только админ
class AttributeTypeUpdateManagerAdmin(BaseModel):
    attribute_name: Optional[AttributeName] = Field(None, example=AttributeName.size)
    class Config:
        from_attributes = True
    
# к read-get имеют доступ все пользователи 
class AttributeTypeRead(AttributeTypeBase):
    attribute_type_id: int
    display_name: str
    class Config:
        from_attributes = True
