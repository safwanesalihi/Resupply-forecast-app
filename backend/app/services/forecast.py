import pandas as pd
import numpy as np
from prophet import Prophet
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.models.sales import CleanSales
from app.db.models.product import Product
from app.db.models.forecast import Forecast

class ForecastService:
    def __init__(self, db: Session):
        self.db = db
    
    def _prepare_data(self, product_id: int) -> Optional[pd.DataFrame]:
        """Prepare sales data for Prophet forecasting"""
        sales = self.db.query(CleanSales).filter(CleanSales.product_id == product_id).order_by(CleanSales.date).all()
        
        if not sales or len(sales) < 5: # Need minimum data points for Prophet
            print(f"Not enough sales data for product {product_id} to generate forecast.")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame([{"ds": s.date, "y": s.quantity} for s in sales])
        
        # Prophet requires 'ds' (date) and 'y' (value) columns
        return df
    
    def generate_forecast(self, product_id: int, periods: int = 30, frequency: str = 'D') -> List[Dict[str, Any]]:
        """Generate forecast for a specific product"""
        # Get sales data
        df = self._prepare_data(product_id)
        
        if df is None:
            return []
        
        try:
            # Initialize and fit Prophet model
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False, # Usually false for daily sales data unless specific daily patterns exist
                seasonality_mode='multiplicative' # Or 'additive' depending on data characteristics
            )
            
            model.fit(df)
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=periods, freq=frequency)
            
            # Generate forecast
            forecast = model.predict(future)
            
            # Extract relevant columns for the future periods
            result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
            
            # Convert to list of dictionaries
            forecast_data = []
            for _, row in result.iterrows():
                forecast_data.append({
                    "date": row['ds'].date(),
                    "predicted_qty": max(0, round(row['yhat'], 2)),  # Ensure non-negative
                    "lower_bound": max(0, round(row['yhat_lower'], 2)),
                    "upper_bound": max(0, round(row['yhat_upper'], 2))
                })
            
            return forecast_data
        except Exception as e:
            print(f"Error generating forecast for product {product_id}: {e}")
            return []
    
    def save_forecast(self, product_id: int, forecast_data: List[Dict[str, Any]]) -> List[Forecast]:
        """Save forecast data to database"""
        # Delete existing future forecasts for this product to avoid duplicates
        # Assuming we only store future forecasts
        today = datetime.now().date()
        self.db.query(Forecast).filter(Forecast.product_id == product_id, Forecast.date >= today).delete()
        
        # Create new forecast records
        forecasts = []
        for data in forecast_data:
            # Only save future forecasts
            if data["date"] >= today:
                forecast = Forecast(
                    product_id=product_id,
                    date=data["date"],
                    predicted_qty=data["predicted_qty"]
                )
                self.db.add(forecast)
                forecasts.append(forecast)
        
        self.db.commit()
        # Refresh objects to get IDs, etc.
        for f in forecasts: 
            self.db.refresh(f)
        return forecasts
    
    def generate_and_save_forecasts(self, product_ids: Optional[List[int]] = None, periods: int = 30, frequency: str = 'D') -> Dict[int, List[Dict[str, Any]]]:
        """Generate and save forecasts for multiple products"""
        if product_ids is None:
            # Get all product IDs
            products = self.db.query(Product.id).all()
            product_ids = [p.id for p in products]
        
        results = {}
        for product_id in product_ids:
            forecast_data = self.generate_forecast(product_id, periods, frequency)
            if forecast_data:
                self.save_forecast(product_id, forecast_data)
                results[product_id] = forecast_data
        
        return results
    
    def check_stock_alerts(self) -> List[Dict[str, Any]]:
        """Check for products that need reordering based on forecasts"""
        alerts = []
        today = datetime.now().date()
        
        # Get all products
        products = self.db.query(Product).all()
        
        for product in products:
            # Get forecast for the next 7 days (or relevant period)
            forecast_period_end = today + timedelta(days=7)
            forecasts = self.db.query(Forecast).filter(
                Forecast.product_id == product.id,
                Forecast.date >= today,
                Forecast.date <= forecast_period_end
            ).all()
            
            # Calculate forecasted usage for the period
            forecasted_usage = sum(f.predicted_qty for f in forecasts)
            
            # Calculate minimum expected stock level at the end of the period
            min_expected_stock = product.stock_level - forecasted_usage
            
            # Check if below reorder threshold
            if min_expected_stock < product.reorder_threshold:
                alerts.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "current_stock": product.stock_level,
                    "forecasted_usage_next_7_days": round(forecasted_usage, 2),
                    "min_expected_stock_next_7_days": round(min_expected_stock, 2),
                    "reorder_threshold": product.reorder_threshold
                })
        
        return alerts

