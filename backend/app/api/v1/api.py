from fastapi import APIRouter
from app.api.v1.endpoints import auth, products, sales, forecasts, alerts

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(forecasts.router, prefix="/forecasts", tags=["forecasts"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])

