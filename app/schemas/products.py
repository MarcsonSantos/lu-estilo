from pydantic import BaseModel
from datetime import date

class ProductBase(BaseModel):
    description: str
    sale_price: float
    barcode: str
    section: str
    stock: int
    expiration_date: date | None = None
    image: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    description: str | None = None
    sale_price: float | None = None
    barcode: str | None = None
    section: str | None = None
    stock: int | None = None
    expiration_date: date | None = None
    image: str | None = None
    is_available: bool | None = None

class ProductOut(ProductBase):
    id: int
    is_available: bool

    class Config:
        from_attributes = True