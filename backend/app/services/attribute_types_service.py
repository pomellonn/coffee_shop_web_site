from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from models import AttributeType
from schemas.attribute_types_schema import (
    AttributeTypeCreateManagerAdmin,
    AttributeTypeUpdateManagerAdmin
)


class AttributeTypesService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_attribute_type_by_id(self, type_id: int)->Optional[AttributeType]:
        result=await self.db.execute(
            select(AttributeType).where(AttributeType.attribute_type_id==type_id)
        )
        return result.scalar_one_or_none()
    
    async def get_attribute_type_by_name(self, type_name: str)->Optional[AttributeType]:
        result=await self.db.execute(
            select(AttributeType).where(AttributeType.attribute_name==type_name)
        )
        return result.scalar_one_or_none()
    
    async def get_all_attribute_types(self)->List[AttributeType]:
        result= await self.db.execute(
            select(AttributeType)
        )
        return result.scalars().all()
    
    async def create_attribute_type(self, type_data: AttributeTypeCreateManagerAdmin)->AttributeType:
        existing=await self.get_attribute_type_by_name(type_data.attribute_name)
        if existing:
            raise ValueError(f"Attribute type '{type_data.attribute_name}' already exists")
        new_type=AttributeType(attribute_name=type_data.attribute_name)
        self.db.add(new_type)
        await self.db.commit()
        await self.db.refresh(new_type)
        return new_type
    
    async def update_attribute_type(self, type_id:int, type_data:AttributeTypeUpdateManagerAdmin)->Optional[AttributeType]:
        attr_type= await self.get_attribute_type_by_id(type_id)
        if not attr_type:
            return None

        if type_data.attribute_name is not None:
            existing=await self.get_attribute_type_by_name(type_data.attribute_name)
            
            if existing and existing.attribute_type_id!=type_id:
                raise ValueError(
                    f"Attribute type '{type_data.attribute_name}' already exists"
                )
            
            attr_type.attribute_name=type_data.attribute_name
        
        await self.db.commit()
        await self.db.refresh(attr_type)
        return attr_type
    
    async def delete_attribute_type(self, type_id:int)->bool:
        attr_type=await self.get_attribute_type_by_id(type_id)
        if not attr_type:
            return False
        
        await self.db.delete(attr_type)
        await self.db.commit()
        return True
        
        