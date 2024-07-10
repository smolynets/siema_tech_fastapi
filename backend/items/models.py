from backend.database import Base
from datetime import datetime as dt

from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, index=True, default=dt.utcnow)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    name = Column(String, index=True)
    price = Column(Float, nullable=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    family = relationship("Family")


class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    month = Column(String)
    count = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product")
