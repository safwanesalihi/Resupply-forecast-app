from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine # Import engine
from app.db.base import Base # Import Base

# Create database tables if they don't exist (optional, Alembic is preferred for production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelligent Stock Management System API",
    description="Backend API for the Intelligent Stock Management System",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json" # Ensure OpenAPI doc path is correct
)

# Set up CORS
# In production, restrict origins to your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to the Intelligent Stock Management System API"}

# Optional: Add startup/shutdown events if needed
# @app.on_event("startup")
# async def startup_event():
#     print("Starting up...")

# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Shutting down...")

# The following is for running directly with uvicorn, not needed if using Docker
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

