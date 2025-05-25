from sqlalchemy.orm import Session
from app.db.models.users import User
from app.schemas.users import UserCreate
from app.core.security import get_password_hash


def get_user_by_id(db: Session, user_id: int):
    """
    Busca um usuário pelo ID.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Busca um usuário pelo email.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_cpf(db: Session, cpf: str):
    """
    Busca um usuário pelo CPF.
    """
    return db.query(User).filter(User.cpf == cpf).first()

def create_user(db: Session, user_in: UserCreate):
    """
    Cria um novo usuário com senha criptografada.
    """
    hashed_password = get_password_hash(user_in.password)
    user = User(email=user_in.email, cpf=user_in.cpf, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

