from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from models import ProductAttributeOptions

from schemas.product_attribute_options_schema import (
    ProductAttributeOptionsCreate,
    ProductAttributeOptionsUpdate
)

class ProductAttributeOptionsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_attribute_option_by_id(self, option_id: int) -> Optional[ProductAttributeOptions]:
        result = await self.db.execute(
            select(ProductAttributeOptions).where(ProductAttributeOptions.option_id == option_id)
        )
        return result.scalar_one_or_none()

    async def get_product_attr_option_by_value(self, option_value: str) -> Optional[ProductAttributeOptions]:
        result = await self.db.execute(
            select(ProductAttributeOptions).where(ProductAttributeOptions.value == option_value)
        )
        return result.scalar_one_or_none()

    async def get_all_product_attr_options(self) -> List[ProductAttributeOptions]:
        result = await self.db.execute(select(ProductAttributeOptions))
        return result.scalars().all()

    async def create_product_attribute_option(self, option: ProductAttributeOptionsCreate) -> ProductAttributeOptions:
        existing = await self.get_product_attr_option_by_value(option.value)
        if existing:
            raise ValueError(f"Option with value '{option.value}' already exists")

        new_option = ProductAttributeOptions(
            value=option.value,
            extra_price=option.extra_price,
            attribute_type_id=option.attribute_type_id,
        )
        self.db.add(new_option)
        await self.db.commit()
        await self.db.refresh(new_option)
        return new_option

    async def update_product_attribute_option(
        self,
        option_id: int,
        option_data: ProductAttributeOptionsUpdate,
    ) -> Optional[ProductAttributeOptions]:
        option = await self.get_product_attribute_option_by_id(option_id)
        if not option:
            return None

        if option_data.value is not None:
            existing = await self.get_product_attr_option_by_value(option_data.value)
            if existing and existing.option_id != option_id:
                raise ValueError(f"Option with value '{option_data.value}' already exists")
            option.value = option_data.value

        if option_data.extra_price is not None:
            option.extra_price = option_data.extra_price

        await self.db.commit()
        await self.db.refresh(option)
        return option

    async def delete_product_attribute_option(self, option_id: int) -> bool:
        option = await self.get_product_attribute_option_by_id(option_id)
        if not option:
            return False
        await self.db.delete(option)
        await self.db.commit()
        return True