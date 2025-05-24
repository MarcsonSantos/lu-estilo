from sqlalchemy.orm import Session
from app.db.models.orders import Order, OrderItem
from app.db.models.products import Product
from app.schemas.orders import OrderCreate, OrderUpdate
from fastapi import HTTPException


def create_order(db: Session, client_id: int, order_in: OrderCreate):
    order = Order(client_id=client_id)
    db.add(order)
    db.flush()

    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto ID {item.product_id} não encontrado")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para o produto {product.description}")
        product.stock -= item.quantity
        db.add(product)

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.sale_price
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def list_orders(db: Session, skip=0, limit=10):
    return db.query(Order).offset(skip).limit(limit).all()


def update_order(db: Session, order: Order, order_in: OrderUpdate):
    order.status = order_in.status
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order: Order):
    db.delete(order)
    db.commit()