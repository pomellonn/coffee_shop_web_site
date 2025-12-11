from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Product, ProductType
from sqlalchemy.exc import IntegrityError
from schemas.product_schema import ProductCreateManagerAdmin, ProductUpdateAdmin


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return await self.db.get(Product, product_id)

    async def get_all_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.db.execute(select(Product).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_product(self, product_in: ProductCreateManagerAdmin) -> Product:
        product = Product(
            name=product_in.name,
            description=product_in.description,
            image_url=product_in.image_url,
            volume=product_in.volume,
            product_type=product_in.product_type,
            price=product_in.price,
        )
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update_product(self, product: Product, updates: dict) -> Product:

        allowed = {
            "name",
            "description",
            "image_url",
            "volume",
            "product_type",
            "price",
        }

        for field, value in updates.items():

            if field not in allowed:
                continue

            if value is None:
                continue

            # product_type conversion
            if field == "product_type":
                try:
                    value = ProductType(value)
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid product_type. Allowed: {[e.value for e in ProductType]}",
                    )

            setattr(product, field, value)

        try:
            self.db.add(product)
            await self.db.commit()
            await self.db.refresh(product)
            return product

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Invalid product data (volume must be > 0, price must be >= 0)",
            )

    async def delete_product(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.commit()
