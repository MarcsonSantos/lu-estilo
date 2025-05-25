from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.orders import OrderCreate, OrderOut, OrderUpdate
from app.crud.orders import create_order, get_order_by_id, list_orders, update_order, delete_order
from app.api.auth import get_current_user
from app.db.models.users import User
from app.db.models.orders import Order

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderOut)
def create(
    client_order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Criar um novo pedido.

    - Apenas clientes logados podem criar pedidos.
    - Valida a existência de estoque para os produtos.
    """
    if not current_user.client:
        raise HTTPException(status_code=403, detail="Apenas clientes podem criar pedidos")
    return create_order(db, current_user.client.id, client_order)


@router.get("/", response_model=list[OrderOut])
def list_all(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listar pedidos.

    - Administradores visualizam todos os pedidos.
    - Clientes visualizam apenas seus próprios pedidos.
    - Suporte a paginação com `skip` e `limit`.
    """
    if current_user.is_admin:
        return list_orders(db, skip, limit)

    if not current_user.client:
        raise HTTPException(status_code=403, detail="Acesso negado: cliente não associado")

    return (
        db.query(Order)
        .filter(Order.client_id == current_user.client.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{id}", response_model=OrderOut)
def get(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obter detalhes de um pedido específico.

    - Clientes podem acessar apenas seus próprios pedidos.
    - Administradores podem acessar qualquer pedido.
    """
    order = get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not current_user.is_admin:
        if not current_user.client or order.client_id != current_user.client.id:
            raise HTTPException(status_code=403, detail="Acesso negado")

    return order


@router.put("/{id}", response_model=OrderOut)
def update(
    id: int,
    order_in: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Atualizar um pedido existente.

    - Clientes podem atualizar apenas seus próprios pedidos.
    - Administradores podem atualizar qualquer pedido.
    """
    order = get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not current_user.is_admin:
        if not current_user.client or order.client_id != current_user.client.id:
            raise HTTPException(status_code=403, detail="Acesso negado")

    return update_order(db, order, order_in)


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Excluir um pedido.

    - Clientes podem excluir apenas seus próprios pedidos.
    - Administradores podem excluir qualquer pedido.
    """
    order = get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not current_user.is_admin:
        if not current_user.client or order.client_id != current_user.client.id:
            raise HTTPException(status_code=403, detail="Acesso negado")

    delete_order(db, order)
    return {"message": "Pedido excluído com sucesso"}
