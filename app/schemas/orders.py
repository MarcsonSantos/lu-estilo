from pydantic import BaseModel
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: list[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    client_id: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: str