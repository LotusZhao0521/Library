from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-in-production"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    DATABASE_URL: str = "sqlite+aiosqlite:///./library.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
