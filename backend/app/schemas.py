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


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None
    price: int


class ProductRead(BaseModel):
    product_id: int
    name: str
    description: str | None
    image_url: str | None
    price: int

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    price: int | None = None
