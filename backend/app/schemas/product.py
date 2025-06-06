from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    stock_level: int = 0
    reorder_threshold: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    stock_level: Optional[int] = None
    reorder_threshold: Optional[int] = None

class ProductInDBBase(ProductBase):
    id: int

    class Config:
        orm_mode = True

class Product(ProductInDBBase):
    pass

