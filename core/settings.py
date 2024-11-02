from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini-2024-07-18"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_ORG_ID: str | None = None
    
    class Config:
        env_file = str(Path(__file__).parent.parent / '.env')
        env_file_encoding = 'utf-8'
        extra = 'allow'  # Allow extra fields in env

def get_settings() -> Settings:
    """Get application settings singleton"""
    return Settings()