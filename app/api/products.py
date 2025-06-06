from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.api.auth import get_current_user
from app.schemas.products import ProductCreate, ProductUpdate, ProductOut
from app.crud.products import *

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
def list_products(skip=0, limit=10, category=None, price=None, available=None, db=Depends(get_db)):
    """
    Listar produtos com suporte a filtros.

    - Filtros disponíveis: categoria, preço e disponibilidade (`available`).
    - Paginação com os parâmetros `skip` e `limit`.
    - Acessível a qualquer usuário autenticado.
    """
    return get_products(db, skip, limit, category, price, available)


@router.get("/{id}", response_model=ProductOut)
def get(id: int, db=Depends(get_db)):
    """
    Obter informações de um produto específico pelo ID.

    - Retorna detalhes do produto.
    - Retorna erro 404 se o produto não for encontrado.
    """
    product = get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@router.post("/", response_model=ProductOut)
def create(product_in: ProductCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Criar um novo produto.

    - Apenas usuários administradores podem realizar essa ação.
    - Requer os campos: descrição, valor de venda, código de barras, seção,
      estoque inicial, data de validade (opcional) e imagens.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return create_product(db, product_in)


@router.put("/{id}", response_model=ProductOut)
def update(id: int, product_in: ProductUpdate, db=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Atualizar um produto existente.

    - Apenas administradores podem atualizar produtos.
    - Retorna erro 404 se o produto não for encontrado.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    product = get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return update_product(db, product, product_in)


@router.delete("/{id}")
def delete(id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Excluir um produto existente.

    - Apenas administradores podem excluir produtos.
    - Retorna erro 404 se o produto não for encontrado.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    product = get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    delete_product(db, product)
    return {"detail": "Produto excluído com sucesso"}
