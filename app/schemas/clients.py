from pydantic import BaseModel, EmailStr
from app.schemas.users import UserOut

class ClientCreate(BaseModel):
    email: EmailStr
    cpf: str
    password: str
    name: str
    address: str
    phone_number: str


class ClientOut(BaseModel):
    id: int
    name: str
    address: str
    phone_number: str
    user: UserOut

    class Config:
        from_attributes = True


class ClientUpdate(BaseModel):
    name: str
    address: str
    phone_number: str
