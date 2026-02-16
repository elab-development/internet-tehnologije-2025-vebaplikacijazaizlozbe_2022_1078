"""
Konfiguracija aplikacije
Učitava podešavanja iz .env fajla
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Glavna konfiguracija aplikacije"""
    
    # Baza podataka
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/izlozbe_db"
    
    # JWT autentifikacija
    SECRET_KEY: str = "kasnije"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS podešavanja
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Art Institute of Chicago API
    ARTIC_API_BASE_URL: str = "https://api.artic.edu/api/v1"

    # Mailsend API
    MAILERSEND_API_KEY: str = "mlsn.bd640940950c7f30835e9ee8dc887bbf032824eb3dbf5b63f05b64268d0b971b"
    MAILERSEND_FROM_EMAIL: str = "info@test-r6ke4n1jjpegon12.mlsender.net"
    MAILERSEND_FROM_NAME: str = "Galerija"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Vraća listu CORS origin-a"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        extra = "allow"


# Globalna instanca podešavanja
settings = Settings()
