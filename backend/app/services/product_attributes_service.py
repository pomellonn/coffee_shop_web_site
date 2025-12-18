from __future__ import annotations

from collections import OrderedDict
from typing import List, Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.product_attributes import ProductAttributes
from models.product_attribute_options import ProductAttributeOptions
from models.attribute_types import AttributeType


class ProductAttributesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_link(self, product_id: int, option_id: int) -> Optional[ProductAttributes]:
        res = await self.db.execute(
            select(ProductAttributes).where(
                ProductAttributes.product_id == product_id,
                ProductAttributes.option_id == option_id,
            )
        )
        return res.scalar_one_or_none()

    async def list_links(self, product_id: int) -> List[ProductAttributes]:
        res = await self.db.execute(
            select(ProductAttributes).where(ProductAttributes.product_id == product_id)
        )
        return res.scalars().all()

    async def add_link(self, product_id: int, option_id: int) -> ProductAttributes:
        existing = await self.get_link(product_id, option_id)
        if existing:
            return existing

        link = ProductAttributes(product_id=product_id, option_id=option_id)
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def delete_link(self, product_id: int, option_id: int) -> bool:
        link = await self.get_link(product_id, option_id)
        if not link:
            return False

        await self.db.delete(link)
        await self.db.commit()
        return True

    async def get_attributes_for_product_user(self, product_id: int) -> Dict[str, Any]:
        """
        Формат под карточку товара:
        {
          "product_id": ...,
          "attributes": [
            {"attribute_type_id":..., "attribute_name":..., "options":[{"option_id":..,"value":..,"extra_price":..}]}
          ]
        }
        """
        stmt = (
            select(
                AttributeType.attribute_type_id,
                AttributeType.attribute_name,
                ProductAttributeOptions.option_id,
                ProductAttributeOptions.value,
                ProductAttributeOptions.extra_price,
            )
            .join(ProductAttributeOptions, ProductAttributeOptions.attribute_type_id == AttributeType.attribute_type_id)
            .join(ProductAttributes, ProductAttributes.option_id == ProductAttributeOptions.option_id)
            .where(ProductAttributes.product_id == product_id)
            .order_by(AttributeType.attribute_name, ProductAttributeOptions.value)
        )

        res = await self.db.execute(stmt)
        rows = res.all()

        grouped: "OrderedDict[int, Dict[str, Any]]" = OrderedDict()
        for attribute_type_id, attribute_name, option_id, value, extra_price in rows:
            bucket = grouped.get(attribute_type_id)
            if bucket is None:
                bucket = {
                    "attribute_type_id": attribute_type_id,
                    "attribute_name": attribute_name,
                    "options": [],
                }
                grouped[attribute_type_id] = bucket

            bucket["options"].append(
                {"option_id": option_id, "value": value, "extra_price": extra_price}
            )

        return {"product_id": product_id, "attributes": list(grouped.values())}