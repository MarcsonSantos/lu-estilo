from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    cpf: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    cpf: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True
