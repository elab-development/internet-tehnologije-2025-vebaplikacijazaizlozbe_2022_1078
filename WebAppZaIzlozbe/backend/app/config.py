
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/izlozbe_db"
    
    SECRET_KEY: str = "kasnije"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    ARTIC_API_BASE_URL: str = "https://api.artic.edu/api/v1"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
