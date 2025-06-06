from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class RawSales(Base):
    __tablename__ = "raw_sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(Date, index=True)
    quantity = Column(Integer)
    
    product = relationship("Product", back_populates="raw_sales")

class CleanSales(Base):
    __tablename__ = "clean_sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(Date, index=True)
    quantity = Column(Integer)
    
    product = relationship("Product", back_populates="clean_sales")

