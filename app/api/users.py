from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.db.models.users import User
from app.schemas.users import UserCreate, UserOut
from app.crud.users import create_user, get_user_by_id, get_user_by_cpf
from app.crud.users import get_user_by_email
from app.api.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/users", response_model=list[UserOut])
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/user", response_model=UserOut)
def get_user(
    id: int = Query(None),
    email: str = Query(None),
    cpf: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/refresh-token")
def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Gera um novo token para o usuário autenticado.
    """
    new_token = create_access_token({"sub": current_user.email})
    return {"access_token": new_token, "token_type": "bearer"}