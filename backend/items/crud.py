
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from backend.config import SERVICE_NAME
from backend.items.models import Item, Product, Family, Sale
from datetime import datetime as dt
from uuid import uuid4
from backend.items.schemas import ProductCreate, ItemUpdate, FamilyCreate
from fastapi import HTTPException

logger = logging.getLogger(f"{SERVICE_NAME}_logger")


class ProductCrud():

    async def get_family(self, db: AsyncSession, family_name: str):
        result = await db.execute(select(Family).where(Family.name == family_name))
        return result.scalars().first()
    

    async def get_families(self, db: AsyncSession, skip: int = 0, limit: int = 10):
        result = await db.execute(select(Family).offset(skip).limit(limit))
        return result.scalars().all()


    async def create_family(self, db: AsyncSession, family_name: str):
        db_family = Family(name=family_name)
        db.add(db_family)
        await db.commit()
        await db.refresh(db_family)
        return db_family


    async def get_sale_by_product(self, db: AsyncSession, month: str, product_id: int):
        result = await db.execute(select(Sale).where(Sale.month == month, Sale.product_id == product_id))
        return result.scalars().first()


    async def get_sales(self, db: AsyncSession, skip: int = 0, limit: int = 10):
        result = await db.execute(select(Sale).offset(skip).limit(limit))
        return result.scalars().all()


    async def create_sales(self, db: AsyncSession, sales: dict, product_id: int):
        for month, count in sales.items():
            sale = await self.get_sale_by_product(db, month, product_id)
            if sale is None:
                db_sale = Sale(month=month, product_id=product_id)
                db.add(db_sale)
                await db.commit()
                await db.refresh(db_sale)
        return True



    async def create_product(self, db: AsyncSession, id: int, name: str, price: int, family_name: str):
        family = await self.get_family(db, family_name)
        if family is None:
            family = await self.create_family(db, family_name)
        db_product = Product(id=id, name=name, price=price, family_id=family.id)
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product


    async def get_products(self, db: AsyncSession, skip: int = 0, limit: int = 10):
        result = await db.execute(select(Product).offset(skip).limit(limit))
        return result.scalars().all()


    async def get_product(self, db: AsyncSession, product_id: int):
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalars().first()


    async def update_item(self, db: AsyncSession, item_id: int, item: ItemUpdate):
        db_item = await get_item(db, item_id)
        if db_item:
            db_item.name = item.name
            db_item.description = item.description
            await db.commit()
            await db.refresh(db_item)
        return db_item


    async def delete_item(self, db: AsyncSession, item_id: int):
        db_item = await get_item(db, item_id)
        if db_item:
            await db.delete(db_item)
            await db.commit()
        return db_item
