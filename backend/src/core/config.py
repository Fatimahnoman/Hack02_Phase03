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

    # MCP settings
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "")

    # Additional settings from .env file
    next_public_api_url: str = os.getenv("NEXT_PUBLIC_API_URL", "http://127.0.0.1:8000")
    agent_temperature: float = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    max_context_tokens: int = int(os.getenv("MAX_CONTEXT_TOKENS", "8000"))
    max_response_tokens: int = int(os.getenv("MAX_RESPONSE_TOKENS", "1000"))
    fallback_response: str = os.getenv("FALLBACK_RESPONSE", "Hi there! 👋 Hello! I'm your AI assistant. How can I help you today?")

    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()