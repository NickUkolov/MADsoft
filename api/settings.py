import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = os.environ.get('POSTGRES_USER', 'user')
    POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD', 'password')
    POSTGRES_DB: str = os.environ.get('POSTGRES_DB', 'meme_db')
    POSTGRES_HOST: str = os.environ.get('DATABASE_HOST', 'db')
    POSTGRES_PORT: str = os.environ.get('DATABASE_PORT', '5432')
    POSTGRES_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    MEDIA_SERVICE_HOST: str = os.environ.get('MEDIA_SERVICE_HOST', 'media_service')
    MEDIA_SERVICE_PORT: str = os.environ.get('MEDIA_SERVICE_PORT', '8001')
    MEDIA_SERVICE_URL: str = f"http://{MEDIA_SERVICE_HOST}:{MEDIA_SERVICE_PORT}"  # noqa

    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    ALLOWED_SIZE_MB: int = 1


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
