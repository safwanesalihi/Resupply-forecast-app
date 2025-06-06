from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    stock_level = Column(Integer, default=0)
    reorder_threshold = Column(Integer, default=0)

    raw_sales = relationship("RawSales", back_populates="product")
    clean_sales = relationship("CleanSales", back_populates="product")
    forecasts = relationship("Forecast", back_populates="product")
    alerts = relationship("StockAlert", back_populates="product")

