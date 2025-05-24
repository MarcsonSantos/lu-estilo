from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models.clients import Client
from app.schemas.clients import ClientCreate


def get_client_by_id(db: Session, client_id: int) -> Optional[Client]:
    return db.query(Client).filter(Client.id == client_id).first()


def get_client_by_name(db: Session, name: str) -> List[Client]:
    return db.query(Client).filter(Client.name.ilike(f"%{name}%")).all()


def get_client_by_address(db: Session, address: str) -> List[Client]:
    return db.query(Client).filter(Client.address.ilike(f"%{address}%")).all()


def get_client_by_phone_number(db: Session, phone_number: str) -> Optional[Client]:
    return db.query(Client).filter(Client.phone_number == phone_number).first()


def get_client_by_user_id(db: Session, user_id: int) -> Optional[Client]:
    return db.query(Client).filter(Client.user_id == user_id).first()


def create_client(db: Session, client_in: ClientCreate, user_id: int) -> Client:
    client = Client(
        name=client_in.name,
        address=client_in.address,
        phone_number=client_in.phone_number,
        user_id=user_id,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
