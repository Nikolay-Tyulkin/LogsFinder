from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    API_HOST: str = os.getenv("HOST", default="0.0.0.0")
    API_PORT: int = int(os.getenv("PORT", default=8000))
    API_TITLE: str = os.getenv("API_TITLE", default="LogsFinder API")
    API_VERSION: str = os.getenv("API_VERSION", default="0.1.0")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", default="LogsFinder API - сервис для поиска логов")
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", default="postgresql+asyncpg://admin:password@db/default_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", default="your_secret_key")
    TEST_LOG_PATH: str = os.getenv("TEST_LOG_PATH", default="test_logs")

settings = Settings()