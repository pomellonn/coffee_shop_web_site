from pydantic import BaseModel


class CoffeeShopCreate(BaseModel):
    name: str
    address: str
    manager_id: int | None = None


class CoffeeShopRead(BaseModel):
    shop_id: int
    name: str
    address: str
    manager_id: int | None

    class Config:
        from_attributes = True


class CoffeeShopUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    manager_id: int | None = None
