import logging
from backend.config import SERVICE_NAME
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from backend.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.items.schemas import ProductCreate, ItemOutSchema, ItemUpdate, ProductSchema, FamilySchema
from backend.items.models import Item, Product
from backend.items.crud import ProductCrud
from typing import List
import pandas as pd
import io

router = APIRouter()

product_crud = ProductCrud()

logger = logging.getLogger(f"{SERVICE_NAME}_logger")

@router.post("/upload-csv/")
async def upload_csv(db: AsyncSession = Depends(get_db_session), file: UploadFile = File(...)):
    contents = file.file.read()
    df = pd.read_csv(io.BytesIO(contents))
    # Strip whitespace from all string values in the DataFrame
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    products_dict = df.to_dict(orient='records')
    for product in products_dict:
        db_product = await product_crud.get_product(db, product["Product ID"])
        if db_product is None:
            sales = {k: v for k, v in product.items() if k not in [
                "Product Name",
                "Product ID",
                "Family",
                "Price"
            ]}
            await product_crud.create_product(
                db,
                id=product["Product ID"],
                name=product["Product Name"],
                price=product["Price"],
                family_name=product["Family"]
            )
            await product_crud.create_sales(db, sales, product["Product ID"])
    return {"message": "Products uploaded successfully"}


@router.get("/products/", response_model=list[ProductSchema])
async def get_all_products(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 10,
):
    return  await product_crud.get_products(db, skip, limit)


@router.get("/families/")
# @router.get("/families/", response_model=list[FamilySchema])
async def get_all_families(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 10,
):
    return  await product_crud.get_families(db, skip, limit)



# @router.post("/", summary="Items", response_model=ItemOutSchema)
# async def create_item_api(
#     item: ItemCreate,
#     session: AsyncSession = Depends(get_db_session),
# ):
#     return await create_item(session, item)


# @router.get("/", response_model=List[ItemOutSchema])
# async def get_item_api(
#     skip: int = 0,
#     limit: int = 10,
#     session: AsyncSession = Depends(get_db_session),
# ):
#     return await get_items(session, skip, limit)


# @router.get("/{item_id}", response_model=ItemOutSchema)
# async def get_item_by_id_api(
#     item_id: int,
#     session: AsyncSession = Depends(get_db_session),
# ):
#     db_item = await get_item(session, item_id)
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item


# @router.put("/{item_id}", response_model=ItemOutSchema)
# async def update_item_api(
#     item_id: int, item: ItemUpdate,
#     session: AsyncSession = Depends(get_db_session),
# ):
#     db_item = await update_item(session, item_id, item)
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item


# @router.delete("/{item_id}", response_model=ItemOutSchema)
# async def delete_item_api(
#     item_id: int,
#     session: AsyncSession = Depends(get_db_session),
# ):
#     db_item = await delete_item(session, item_id)
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item
