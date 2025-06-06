import os
from pydantic import BaseSettings, PostgresDsn
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: PostgresDsn = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/stock_management")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Dynamics BC
    DYNAMICS_BC_BASE_URL: str = os.getenv("DYNAMICS_BC_BASE_URL", "https://api.businesscentral.dynamics.com")
    DYNAMICS_BC_COMPANY_ID: str = os.getenv("DYNAMICS_BC_COMPANY_ID", "your-company-id")
    DYNAMICS_BC_ENVIRONMENT: str = os.getenv("DYNAMICS_BC_ENVIRONMENT", "your-environment")
    DYNAMICS_BC_CLIENT_ID: str = os.getenv("DYNAMICS_BC_CLIENT_ID", "your-client-id")
    DYNAMICS_BC_CLIENT_SECRET: str = os.getenv("DYNAMICS_BC_CLIENT_SECRET", "your-client-secret")
    DYNAMICS_BC_TENANT_ID: str = os.getenv("DYNAMICS_BC_TENANT_ID", "your-tenant-id")

settings = Settings()

