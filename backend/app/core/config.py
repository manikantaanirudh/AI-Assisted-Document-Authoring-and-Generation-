from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LLM
    LLM_PROVIDER: str = "gemini"  # openai or gemini
    LLM_API_KEY: str
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # Application
    EXPORT_TMP_DIR: str = "./exports"
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

