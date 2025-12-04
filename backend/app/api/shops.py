from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from backend.app.models.models import CoffeeShop
from schemas import CoffeeShopRead, CoffeeShopCreate, CoffeeShopUpdate

router = APIRouter(prefix="/shops", tags=["shops"])


@router.post("/", response_model=CoffeeShopRead, summary="Create a new CoffeeShop")
async def create_shop(data: CoffeeShopCreate, db: AsyncSession = Depends(get_session)):
    shop = CoffeeShop(**data.dict())
    db.add(shop)
    await db.commit()
    await db.refresh(shop)
    return shop


@router.get("/", response_model=list[CoffeeShopRead], summary="Get all CoffeeShops")
async def get_shops(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CoffeeShop))
    shops = result.scalars().all()
    return shops


# чтение данных кофейни по id
@router.get("/{shop_id}", response_model=CoffeeShopRead, summary="Get CoffeeShop by ID")
async def get_shop(shop_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CoffeeShop).where(CoffeeShop.shop_id == shop_id))
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="CoffeeShop not found")
    return shop


# Обновление данных кофейни по id
@router.put("/{shop_id}", response_model=CoffeeShopRead, summary="Update CoffeeShop info by ID")
async def update_shop(
    shop_id: int, data: CoffeeShopUpdate, db: AsyncSession = Depends(get_session)
):
    shop = await db.get(CoffeeShop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="CoffeeShop not found")

    if data.manager_id:
        manager = await db.get(User, data.manager_id)
        if not manager or manager.role != "manager":
            raise HTTPException(status_code=400, detail="Manager not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(shop, field, value)

    db.add(shop)
    await db.commit()
    await db.refresh(shop)
    return shop


# Удаление кофейни по id
@router.delete("/{shop_id}", summary="Delete CoffeeShop by ID")
async def delete_shop(shop_id: int, db: AsyncSession = Depends(get_session)):
    shop = await db.get(CoffeeShop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="CoffeeShop not found")

    await db.delete(shop)
    await db.commit()
    return {"detail": "CoffeeShop deleted"}
