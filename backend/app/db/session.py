from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from contextlib import contextmanager
from core.config import settings
from db.base import Base


ASYNC_DATABASE_URL = settings.DATABASE_URL
SYNC_DATABASE_URL = settings.DATABASE_URL_SYNC

if not ASYNC_DATABASE_URL or not SYNC_DATABASE_URL:
    raise ValueError("DATABASE_URL or DATABASE_URL_SYNC not set")


# ASYNC (FastAPI)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


AsyncDBDependency = Annotated[AsyncSession, Depends(get_session)]


# SYNC (sqladmin)
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
)

@contextmanager
def get_sync_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()