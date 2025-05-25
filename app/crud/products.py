from sqlalchemy.orm import Session
from app.db.models.products import Product
from app.schemas.products import ProductCreate, ProductUpdate

def get_product_by_id(db: Session, id: int):
    """
    Retorna um produto específico pelo ID.
    """
    return db.query(Product).filter(Product.id == id).first()

def get_products(db: Session, skip=0, limit=10, category=None, price=None, available=None):
    """
    Lista produtos com suporte a filtros e paginação.
    """
    query = db.query(Product)
    if category:
        query = query.filter(Product.section == category)
    if price is not None:
        query = query.filter(Product.sale_price <= price)
    if available is not None:
        query = query.filter(Product.is_available == available)
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product_in: ProductCreate):
    """
    Cria um novo produto a partir dos dados fornecidos.
    """
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product: Product, product_in: ProductUpdate):
    """
    Atualiza campos de um produto existente.
    """
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product: Product):
    """
    Remove um produto do banco de dados.
    """
    db.delete(product)
    db.commit()
