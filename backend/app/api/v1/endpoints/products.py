from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.v1.deps import get_db, get_current_user
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.db.models.product import Product as ProductModel
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Product])
def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
) -> List[Product]:
    """
    Get all products with optional filtering
    """
    query = db.query(ProductModel)
    
    if category:
        query = query.filter(ProductModel.category == category)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Product:
    """
    Get a specific product by ID
    """
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Product:
    """
    Create a new product
    """
    db_product = ProductModel(**product_in.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Product:
    """
    Update a product
    """
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.add(product) # Add to session before commit
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", response_model=Product)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Product:
    """
    Delete a product
    """
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    db.delete(product)
    db.commit()
    # Return the deleted object data (it's still in memory)
    return product

