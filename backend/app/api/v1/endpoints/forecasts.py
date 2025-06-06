from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import date

from app.api.v1.deps import get_db, get_current_user
from app.schemas.forecast import Forecast, ForecastGenerate
from app.db.models.forecast import Forecast as ForecastModel
from app.db.models.user import User
from app.services.forecast import ForecastService

router = APIRouter()

def run_forecast_generation(db: Session, product_ids: Optional[List[int]], periods: int, frequency: str):
    """Helper function to run forecast generation in the background."""
    forecast_service = ForecastService(db)
    try:
        results = forecast_service.generate_and_save_forecasts(
            product_ids=product_ids,
            periods=periods,
            frequency=frequency
        )
        print(f"Background forecast generation complete for {len(results)} products.")
    except Exception as e:
        print(f"Error during background forecast generation: {e}")
        # Add more robust error logging/handling here

@router.get("/", response_model=List[Forecast])
def get_forecasts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
) -> List[Forecast]:
    """
    Get forecasts with optional filtering
    """
    query = db.query(ForecastModel)
    
    if product_id:
        query = query.filter(ForecastModel.product_id == product_id)
    if start_date:
        query = query.filter(ForecastModel.date >= start_date)
    if end_date:
        query = query.filter(ForecastModel.date <= end_date)
    
    return query.order_by(ForecastModel.date).offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=List[Forecast])
def get_product_forecast(
    product_id: int,
    db: Session = Depends(get_db),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
) -> List[Forecast]:
    """
    Get forecasts for a specific product
    """
    query = db.query(ForecastModel).filter(ForecastModel.product_id == product_id)
    
    if start_date:
        query = query.filter(ForecastModel.date >= start_date)
    if end_date:
        query = query.filter(ForecastModel.date <= end_date)
    
    forecasts = query.order_by(ForecastModel.date).all()
    
    # Don't raise 404 if no forecasts exist, just return empty list
    # if not forecasts:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="No forecasts found for this product"
    #     )
    
    return forecasts

@router.post("/generate", status_code=status.HTTP_202_ACCEPTED)
def generate_forecasts(
    forecast_params: ForecastGenerate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Trigger background task to generate new forecasts for products
    """
    try:
        # Add the forecast generation task to the background
        background_tasks.add_task(
            run_forecast_generation,
            db,
            forecast_params.product_ids,
            forecast_params.periods,
            forecast_params.frequency
        )
        
        return {
            "status": "accepted",
            "message": "Forecast generation started in the background."
        }
    
    except Exception as e:
        print(f"Error initiating forecast generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start forecast generation: {str(e)}"
        )

