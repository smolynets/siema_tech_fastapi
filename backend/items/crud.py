import logging
from sqlalchemy import select
from backend.config import SERVICE_NAME
from backend.items.models import Item, Product, Family, Sale
from backend.items.schemas import ProductCreate, ItemUpdate, FamilyCreate, FamilyUpdate, ProductUpdate
from fastapi import HTTPException
from sqlalchemy.orm import Session

logger = logging.getLogger(f"{SERVICE_NAME}_logger")

class ProductCrud:

    def get_family(self, db: Session, id: int):
        result = db.execute(select(Family).where(Family.id == id))
        return result.scalars().first()

    def get_family_by_name(self, db: Session, family_name: str):
        result = db.execute(select(Family).where(Family.name == family_name))
        return result.scalars().first()
    
    def get_families(self, db: Session, skip: int = 0, limit: int = 10):
        result = db.execute(select(Family).offset(skip).limit(limit))
        return result.scalars().all()

    def create_family(self, db: Session, family_name: str):
        db_family = Family(name=family_name)
        db.add(db_family)
        db.commit()
        db.refresh(db_family)
        return db_family


    def update_family(self, db: Session, id: int, item: FamilyUpdate):
        db_item = self.get_family(db, id)
        if db_item:
            db_item.name = item.name
            db.commit()
            db.refresh(db_item)
        return db_item

    def get_sale_by_product(self, db: Session, month: str, product_id: int):
        result = db.execute(select(Sale).where(Sale.month == month, Sale.product_id == product_id))
        return result.scalars().first()

    def get_sale_by_id(self, db: Session, id: int):
        result = db.execute(select(Sale).where(Sale.id == id))
        return result.scalars().first()

    def get_sales(self, db: Session, skip: int = 0, limit: int = 10):
        result = db.execute(select(Sale).offset(skip).limit(limit))
        return result.scalars().all()

    def create_sales(self, db: Session, sales: dict, product_id: int):
        for month, count in sales.items():
            sale = self.get_sale_by_product(db, month, product_id)
            if sale is None:
                db_sale = Sale(month=month, product_id=product_id, count=count)
                db.add(db_sale)
                db.commit()
                db.refresh(db_sale)
        return True

    def create_product(self, db: Session, id: int, name: str, price: int, family_name: str):
        family = self.get_family_by_name(db, family_name)
        if family is None:
            family = self.create_family(db, family_name)
        db_product = Product(id=id, name=name, price=price, family_id=family.id)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def get_products(self, db: Session, skip: int = 0, limit: int = 10):
        result = db.execute(select(Product).offset(skip).limit(limit))
        return result.scalars().all()

    def get_product(self, db: Session, product_id: int):
        result = db.execute(select(Product).where(Product.id == product_id))
        return result.scalars().first()

    def update_product(self, db: Session, id: int, item: ProductUpdate):
        db_item = self.get_product(db, id)
        if db_item:
            db_item.id = item.id
            db_item.name = item.name
            db_item.price = item.price
            db.commit()
            db.refresh(db_item)
        return db_item

    def delete_sale(self, db: Session, id: int):
        db_item = self.get_sale_by_id(db, id)
        if db_item:
            db.delete(db_item)
            db.commit()
        return db_item

    def delete_product(self, db: Session, id: int):
        db_item = self.get_product(db, id)
        if db_item:
            db.delete(db_item)
            db.commit()
        return db_item

    def delete_family(self, db: Session, id: int):
        db_item = self.get_family(db, id)
        if db_item:
            db.delete(db_item)
            db.commit()
        return db_item
