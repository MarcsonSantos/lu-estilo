from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.clients import ClientCreate, ClientOut, ClientUpdate
from app.db.models.clients import Client
from app.db.models.users import User
from app.crud.clients import create_client, get_client_by_id
from app.crud.users import get_user_by_email, get_user_by_cpf
from app.api.auth import get_current_user

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=list[ClientOut])
def list_clients(
    name: str | None = Query(default=None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")

    query = db.query(Client)
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_new_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
):
    if get_user_by_email(db, client_in.email):
        raise HTTPException(status_code=400, detail="Email já está em uso.")
    if get_user_by_cpf(db, client_in.cpf):
        raise HTTPException(status_code=400, detail="CPF já está em uso.")

    from app.crud.users import create_user
    user = create_user(db, client_in)

    return create_client(db, client_in, user_id=user.id)


@router.get("/{id}", response_model=ClientOut)
def get_client(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if not current_user.is_admin and client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return client


@router.put("/{id}", response_model=ClientOut)
def update_client(
    id: int,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if not current_user.is_admin and client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    for field, value in client_in.model_dump(exclude_unset=True).items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem excluir clientes")

    client = get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(client)
    db.commit()
