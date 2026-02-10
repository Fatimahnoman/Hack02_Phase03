from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./chat_app.db"  # Default for development
    )

    db_echo: bool = os.getenv("DB_ECHO", "True").lower() == "true"  # Set to True for SQL query logging

    # API settings
    api_prefix: str = "/api"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # CORS settings
    allowed_origins: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Neon Serverless PostgreSQL specific settings
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    db_max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    db_pool_timeout: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    db_pool_recycle: int = int(os.getenv("DB_POOL_RECYCLE", "300"))  # 5 minutes

    # Chat settings
    max_message_length: int = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))
    max_conversation_history: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "50"))

    # Auth settings (from original Phase II)
    secret_key: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # AI settings - Now using Cohere API
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    cohere_model: str = os.getenv("COHERE_MODEL", "command-r")
    agent_temperature: float = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    max_context_tokens: int = int(os.getenv("MAX_CONTEXT_TOKENS", "8000"))
    max_response_tokens: int = int(os.getenv("MAX_RESPONSE_TOKENS", "1000"))
    fallback_response: str = os.getenv("FALLBACK_RESPONSE", "I'm having trouble responding right now. Could you try rephrasing?")

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"  # Allow extra fields in .env that are not explicitly defined
    }


# Create a singleton instance of settings
settings = Settings()