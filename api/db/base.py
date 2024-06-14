from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_async_engine(settings.POSTGRES_URL, future=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_session() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
