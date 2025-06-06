from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class SalesBase(BaseModel):
    product_id: int
    date: date
    quantity: int

class SalesCreate(SalesBase):
    pass

class SalesUpdate(BaseModel):
    date: Optional[date] = None
    quantity: Optional[int] = None

class SalesInDBBase(SalesBase):
    id: int

    class Config:
        orm_mode = True

class RawSales(SalesInDBBase):
    pass

class CleanSales(SalesInDBBase):
    pass

class SalesImport(BaseModel):
    start_date: date
    end_date: date
    product_ids: Optional[List[int]] = None

