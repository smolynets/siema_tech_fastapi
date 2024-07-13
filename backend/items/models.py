from datetime import datetime as dt

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
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
    count = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product")
