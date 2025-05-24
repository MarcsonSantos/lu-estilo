from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text
from app.db.base_class import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    sale_price = Column(Float, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    section = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    expiration_date = Column(Date, nullable=True)
    image = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)