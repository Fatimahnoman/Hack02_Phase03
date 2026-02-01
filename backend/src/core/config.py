import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    database_echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    openai_api_base_url: str = os.getenv("OPENAI_API_BASE_URL", "")

    # Application settings
    app_name: str = "Agent-Orchestrated Task Management"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = 30  # Default value

    # MCP settings
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "")

    # Additional settings from .env file
    next_public_api_url: str = os.getenv("NEXT_PUBLIC_API_URL", "http://127.0.0.1:8000")
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    # Numeric settings with error handling
    agent_temperature: float
    max_context_tokens: int
    max_response_tokens: int
    fallback_response: str = os.getenv("FALLBACK_RESPONSE", "Hi there! 👋 Hello! I'm your AI assistant. How can I help you today?")

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields that don't match

    def model_post_init(self, __context):
        # Set defaults and handle potential conversion errors
        try:
            temp_val = os.getenv("AGENT_TEMPERATURE", "0.7")
            self.agent_temperature = float(temp_val)
        except (ValueError, TypeError):
            self.agent_temperature = 0.7

        try:
            tokens_val = os.getenv("MAX_CONTEXT_TOKENS", "8000")
            self.max_context_tokens = int(tokens_val)
        except (ValueError, TypeError):
            self.max_context_tokens = 8000

        try:
            resp_tokens_val = os.getenv("MAX_RESPONSE_TOKENS", "1000")
            self.max_response_tokens = int(resp_tokens_val)
        except (ValueError, TypeError):
            self.max_response_tokens = 1000

        try:
            expire_minutes_val = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
            self.access_token_expire_minutes = int(expire_minutes_val)
        except (ValueError, TypeError):
            self.access_token_expire_minutes = 30

    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()