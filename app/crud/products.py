# app/crud/products.py
from sqlalchemy.orm import Session
from app.db.models.products import Product
from app.schemas.products import ProductCreate, ProductUpdate

def get_product_by_id(db: Session, id: int):
    return db.query(Product).filter(Product.id == id).first()

def get_products(db: Session, skip=0, limit=10, category=None, price=None, available=None):
    query = db.query(Product)
    if category:
        query = query.filter(Product.section == category)
    if price is not None:
        query = query.filter(Product.sale_price <= price)
    if available is not None:
        query = query.filter(Product.is_available == available)
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product_in: ProductCreate):
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product: Product, product_in: ProductUpdate):
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()