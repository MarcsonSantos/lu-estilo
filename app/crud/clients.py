from sqlalchemy.orm import Session
from app.db.models.clients import User
from app.schemas.clients import UserCreate
from app.core.security import get_password_hash


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_cpf(db: Session, cpf: str):
    return db.query(User).filter(User.cpf == cpf).first()

def create_user(db: Session, user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)
    user = User(email=user_in.email, cpf=user_in.cpf, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
