from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.v1.deps import get_db, get_current_user
from app.schemas.alert import Alert, AlertUpdate
from app.db.models.alert import StockAlert
from app.db.models.user import User
from app.services.forecast import ForecastService # Import ForecastService to check alerts

router = APIRouter()

@router.get("/", response_model=List[Alert])
def get_alerts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
) -> List[Alert]:
    """
    Get stock alerts with optional filtering
    """
    query = db.query(StockAlert)
    
    if product_id:
        query = query.filter(StockAlert.product_id == product_id)
    if status:
        query = query.filter(StockAlert.status == status)
    
    return query.order_by(StockAlert.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/check", response_model=List[dict])
def check_stock_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[dict]:
    """
    Check for products that need reordering based on forecasts and create alerts.
    Returns a list of potential alert situations.
    """
    forecast_service = ForecastService(db)
    potential_alerts = forecast_service.check_stock_alerts()
    
    created_alerts_info = []
    # Create alert records for products below threshold if not already alerted recently
    for alert_data in potential_alerts:
        # Check if an open alert already exists for this product
        existing_alert = db.query(StockAlert).filter(
            StockAlert.product_id == alert_data["product_id"],
            StockAlert.alert_type == "low_stock",
            StockAlert.status == "new" # Or consider other statuses like 'acknowledged'
        ).first()
        
        if not existing_alert:
            alert_message = (
                f"Product {alert_data["product_name"]} (ID: {alert_data["product_id"]}) "
                f"is forecasted to drop below reorder threshold ({alert_data["reorder_threshold"]}). "
                f"Current: {alert_data["current_stock"]:.2f}, "
                f"Forecasted usage (7d): {alert_data["forecasted_usage_next_7_days"]:.2f}, "
                f"Min expected stock (7d): {alert_data["min_expected_stock_next_7_days"]:.2f}."
            )
            alert = StockAlert(
                product_id=alert_data["product_id"],
                alert_type="low_stock",
                message=alert_message,
                status="new"
            )
            db.add(alert)
            created_alerts_info.append(alert_data) # Add info about the created alert
        else:
            # Optionally update the existing alert message or timestamp
            pass 

    if created_alerts_info:
        try:
            db.commit()
            print(f"Created {len(created_alerts_info)} new low stock alerts.")
        except Exception as e:
            db.rollback()
            print(f"Error committing new stock alerts: {e}")
            # Return the potential alerts even if DB commit failed for info
            return potential_alerts
            
    # Return the list of products currently identified as needing alerts
    return potential_alerts

@router.put("/{alert_id}/status", response_model=Alert)
def update_alert_status(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Alert:
    """
    Update alert status (e.g., to 'acknowledged', 'resolved')
    """
    alert = db.query(StockAlert).filter(StockAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    # Add validation for allowed status transitions if needed
    alert.status = alert_update.status
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    return alert

