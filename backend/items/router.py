import logging
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from backend.database import get_db
from backend.items.schemas import (
    ProductCreate,
    ItemOutSchema,
    ItemUpdate,
    ProductSchema,
    FamilySchema,
    FamilyUpdate,
    FamilyOutSchema,
    ProductUpdate,
    ProductOutSchema,
    SaleOutSchema,
    SaleUpdate
)
from backend.items.models import Item, Product
from backend.items.crud import ProductCrud
from typing import List
import pandas as pd
import io
from sqlalchemy.orm import Session

router = APIRouter()

product_crud = ProductCrud()

logger = logging.getLogger("SERVICE_NAME_logger")  # Adjust SERVICE_NAME as needed

@router.post("/upload-csv/")
def upload_csv(db: Session = Depends(get_db), file: UploadFile = File(...)):
    contents = file.file.read()
    df = pd.read_csv(io.BytesIO(contents))
    # Strip whitespace from all string values in the DataFrame
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    products_dict = df.to_dict(orient='records')
    for product in products_dict:
        db_product = product_crud.get_product(db, product["Product ID"])
        if db_product is None:
            sales = {k: v for k, v in product.items() if k not in [
                "Product Name",
                "Product ID",
                "Family",
                "Price"
            ]}
            product_crud.create_product(
                db,
                id=product["Product ID"],
                name=product["Product Name"],
                price=product["Price"],
                family_name=product["Family"]
            )
            product_crud.create_sales(db, sales, product["Product ID"])
    return {"message": "Products uploaded successfully"}

@router.get("/products/", response_model=list[ProductSchema])
def get_all_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    return product_crud.get_products(db, skip, limit)


@router.get("/product/{id}")
def get_product_by_id(
    id: int,
    db: Session = Depends(get_db)
):  
    db_item = product_crud.get_product(db, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_item


@router.put("/product/{id}", response_model=ProductOutSchema)
def update_product_api(
    id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    db_item = product_crud.update_product(db, id, product)
    if not db_item:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_item


@router.get("/families/")
def get_all_families(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    return product_crud.get_families(db, skip, limit)


@router.get("/family/{id}")
def get_family_by_id(
    id: int,
    db: Session = Depends(get_db)
):  
    db_item = product_crud.get_family(db, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Family not found")
    return db_item


@router.get("/sales/")
def get_all_sales(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    return product_crud.get_sales(db, skip, limit)


@router.get("/sale/{id}")
def get_sale_by_id(
    id: int,
    db: Session = Depends(get_db)
):  
    db_item = product_crud.get_sale_by_id(db, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_item


@router.put("/sale/{id}", response_model=SaleOutSchema)
def update_sale_api(
    id: int,
    family: SaleUpdate,
    db: Session = Depends(get_db)
):
    db_item = product_crud.update_sale(db, id, family)
    if not db_item:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_item   


@router.put("/family/{id}", response_model=FamilyOutSchema)
def update_family_api(
    id: int,
    family: FamilyUpdate,
    db: Session = Depends(get_db)
):
    db_item = product_crud.update_family(db, id, family)
    if not db_item:
        raise HTTPException(status_code=404, detail="Family not found")
    return db_item


@router.delete("/delete_sale/{id}")
def delete_sale(
    id: int,
    db: Session = Depends(get_db),
):
    db_item = product_crud.delete_sale(db, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_item

@router.delete("/delete_product/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db),
):
    db_item = product_crud.delete_product(db, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_item

@router.delete("/delete_family/{id}")
def delete_family(
    id: int,
    db: Session = Depends(get_db),
):
    db_item = product_crud.delete_family(db, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Family not found")
    return db_item
