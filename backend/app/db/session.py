from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session
