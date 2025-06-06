from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ForecastBase(BaseModel):
    product_id: int
    date: date
    predicted_qty: float

class ForecastCreate(ForecastBase):
    pass

class ForecastInDBBase(ForecastBase):
    id: int

    class Config:
        orm_mode = True

class Forecast(ForecastInDBBase):
    pass

class ForecastGenerate(BaseModel):
    product_ids: Optional[List[int]] = None
    periods: int = 30
    frequency: str = "D"  # D=daily, W=weekly, M=monthly

