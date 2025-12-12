from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings
from db.base import Base

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")


engine = create_async_engine(DATABASE_URL, echo=True)


async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Use Base from db.base (SQLAlchemy 2.0 DeclarativeBase)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


AsyncDBDependency = Annotated[AsyncSession, Depends(get_session)]
