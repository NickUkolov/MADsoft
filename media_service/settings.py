import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MINIO_HOST: str = os.environ.get('MINIO_HOST', 'localhost')
    MINIO_PORT: str = os.environ.get('MINIO_PORT', '9000')
    MINIO_ROOT_USER: str = os.environ.get('MINIO_ROOT_USER', 'minioadmin')
    MINIO_ROOT_PASSWORD: str = os.environ.get('MINIO_ROOT_PASSWORD', 'minioadmin')
    MINIO_BUCKET: str = os.environ.get('MINIO_BUCKET', 'memes')
    MINIO_URI: str = f"http://{MINIO_HOST}:{MINIO_PORT}/"  # noqa
    MINIO_URL_TTL: int = os.environ.get('MINIO_URL_TTL', 3600)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
