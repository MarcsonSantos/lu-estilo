from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.clients import User
from app.schemas.clients import UserCreate, UserOut
from app.crud.clients import create_user, get_user_by_id, get_user_by_cpf
from app.crud.clients import get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/user", response_model=UserOut)
def get_user(
        id: int = Query(None),
        email: str = Query(None),
        cpf: str = Query(None),
        db: Session = Depends(get_db)
):
    if id:
        user = get_user_by_id(db, id)
    elif email:
        user = get_user_by_email(db, email)
    elif cpf:
        user = get_user_by_cpf(db, cpf)
    else:
        raise HTTPException(status_code=400, detail="Informe id, email ou cpf")

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email já registrado")

    user = create_user(db, user_in)
    return user