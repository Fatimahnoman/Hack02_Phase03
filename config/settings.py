from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Server settings
    server_host: str = os.getenv("SERVER_HOST", "localhost")
    server_port: int = int(os.getenv("SERVER_PORT", "3000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default to SQLite for testing
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    db_pool_timeout: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))

    # Neon Serverless PostgreSQL settings
    neon_database_url: Optional[str] = os.getenv("NEON_DATABASE_URL")

    class Config:
        env_file = ".env"

settings = Settings()