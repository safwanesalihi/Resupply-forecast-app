from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    product_id: int
    alert_type: str
    message: str
    status: str = "new"

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    status: str

class AlertInDBBase(AlertBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Alert(AlertInDBBase):
    pass

