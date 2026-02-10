import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Also load .env.local if present so local overrides are picked up
load_dotenv(".env.local", override=True)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///test.db")  # Use test.db in current working directory
    # Allow either DATABASE_ECHO or DB_ECHO in env files
    database_echo: bool = os.getenv("DATABASE_ECHO", os.getenv("DB_ECHO", "false")).lower() == "true"

    # Cohere settings (replacing OpenAI)
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    cohere_model: str = os.getenv("COHERE_MODEL", "command-r")
    
    # OpenRouter settings
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

    # Application settings
    app_name: str = "Agent-Orchestrated Task Management"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS settings
    allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # MCP settings
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "")

    # Additional settings from .env file
    next_public_api_url: str = os.getenv("NEXT_PUBLIC_API_URL", "http://127.0.0.1:8000")
    agent_temperature: float = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    max_context_tokens: int = int(os.getenv("MAX_CONTEXT_TOKENS", "8000"))
    max_response_tokens: int = int(os.getenv("MAX_RESPONSE_TOKENS", "1000"))
    fallback_response: str = os.getenv("FALLBACK_RESPONSE", "I encountered an error processing your request.")

    model_config = {
        "case_sensitive": True,
        "extra": "allow"  # Allow extra fields in .env that are not explicitly defined
    }


# Global settings instance
settings = Settings()