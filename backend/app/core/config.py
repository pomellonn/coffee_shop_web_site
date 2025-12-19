# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str
    DATABASE_URL_SYNC: str | None = None

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env")
        env_file_encoding = "utf-8"


settings = Settings()
