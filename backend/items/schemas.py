from datetime import datetime
from enum import Enum

from pydantic import BaseModel, validator


class ProductCreate(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True


class ProductOutSchema(BaseModel):
    id: int
    name: str
    price: int
    family_id: int

    class Config:
        orm_mode = True

class FamilyCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class FamilyOutSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class FamilyUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True


class FamilySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SaleOutSchema(BaseModel):
    id: int
    month: str
    count: int
    product_id: int

    class Config:
        orm_mode = True


class SaleUpdate(BaseModel):
    month: str
    count: int

    class Config:
        orm_mode = True