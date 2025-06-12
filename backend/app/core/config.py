from typing import Optional, Dict, Any, List
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"  # In production, use a secure key and store in environment
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "app"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/stock_management"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Dynamics BC settings
    DYNAMICS_BC_BASE_URL: str = "https://api.businesscentral.dynamics.com"
    DYNAMICS_BC_COMPANY_ID: str = "your-dynamics-company-guid"
    DYNAMICS_BC_ENVIRONMENT: str = "Production"
    DYNAMICS_BC_CLIENT_ID: str = "your-azure-app-client-id"
    DYNAMICS_BC_CLIENT_SECRET: str = "your-azure-app-client-secret"
    DYNAMICS_BC_TENANT_ID: str = "your-azure-ad-tenant-id"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

