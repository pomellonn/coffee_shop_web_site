from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from backend.app.models.models import Product
from schemas import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


# Создание нового продукта
@router.post("/", response_model=ProductRead, summary="Create a new Product")
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_session)):
    product = Product(**data.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


# Получить все продукты
@router.get("/", response_model=list[ProductRead], summary="Get all Products")
async def get_products(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Product))
    return result.scalars().all()


# Получить продукт по id
@router.get("/{product_id}", response_model=ProductRead, summary="Get Product by ID")
async def get_product(product_id: int, db: AsyncSession = Depends(get_session)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Обновить данные о продукте по id
@router.put("/{product_id}", response_model=ProductRead, summary="Update Product info by ID")
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_session),
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


# Удаление продукта по id
@router.delete("/{product_id}", summary="Delete Product by ID")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {"detail": "Product deleted"}