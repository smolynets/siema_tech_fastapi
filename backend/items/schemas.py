from datetime import datetime
from enum import Enum
from pydantic import BaseModel, validator


class ProductCreate(BaseModel):
    id: int
    name: str
    price: int

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


class ItemOutSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime


class ItemUpdate(BaseModel):
    name: str
    description: str

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