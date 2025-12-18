import os
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))
env_path = ROOT / ".env.test"
if env_path.exists():
    load_dotenv(env_path)

from app.main import app
from app.db.base import Base
from app.db.session import get_session
from app.core.security import create_access_token, get_password_hash
from app.models import User, UserRole, CoffeeShop

TEST_DB_URL = os.getenv("DATABASE_URL")


engine_test = create_async_engine(TEST_DB_URL, poolclass=NullPool)
AsyncSessionTest = async_sessionmaker(engine_test, expire_on_commit=False)


async def override_get_session() -> AsyncSession:
    async with AsyncSessionTest() as session:
        yield session


# override the dependency in the app so tests use the test DB
app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session")
def anyio_backend():
    """Tell anyio to use asyncio as backend for async tests"""
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Create/drop all tables once per test session.

    This leaves a clean schema and avoids relying on migrations in tests.
    """
    async with engine_test.begin() as conn:
        # Drop the public schema with CASCADE to remove objects created outside SQLAlchemy
        # (some DB initialization scripts create tables not present in MetaData)
        try:
            await conn.run_sync(lambda sync_conn: sync_conn.execute(text("DROP SCHEMA public CASCADE")))
            await conn.run_sync(lambda sync_conn: sync_conn.execute(text("CREATE SCHEMA public")))
        except Exception:
            # If DROP SCHEMA fails (e.g., permissions), fallback to best-effort drop_all
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    """Provides a transactional AsyncSession for a test (commits are allowed).

    If you want finer-grained isolation, wrap tests in nested transactions.
    """
    async with AsyncSessionTest() as session:
        yield session


@pytest.fixture(autouse=True)
async def clean_tables():
    """Truncate all tables before each test to keep tests isolated.

    Uses RESTART IDENTITY and CASCADE to handle FK dependencies and reset sequences.
    """
    table_names = ", ".join([t.name for t in Base.metadata.sorted_tables])
    if table_names:
        async with engine_test.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute(text(f"TRUNCATE {table_names} RESTART IDENTITY CASCADE")))
    yield


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def admin_user(db_session: AsyncSession):
    user = User(
        email="admin@example.com",
        password_hash=get_password_hash("adminpass"),
        role=UserRole.admin,
        name="Admin",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
@pytest.fixture
async def manager_user(db_session: AsyncSession, admin_user):
    manager = User(
        email="manager@example.com",
        password_hash=get_password_hash("managerpass"),
        role=UserRole.manager,
        name="Manager",
    )
    db_session.add(manager)
    await db_session.commit()
    await db_session.refresh(manager)

    shop = CoffeeShop(
        name="Test Shop",
        address="Test address",
        manager_id=manager.user_id,
    )
    db_session.add(shop)
    await db_session.commit()
    await db_session.refresh(shop)
    return manager


@pytest.fixture
async def customer_user(db_session: AsyncSession):
    user = User(
        email="customer@example.com",
        password_hash=get_password_hash("custpass"),
        role=UserRole.customer,
        name="Customer",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def token_headers_admin(admin_user: User):
    token = create_access_token(
        {"user_id": admin_user.user_id, "sub": str(admin_user.email), "role": admin_user.role.value}
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def token_headers_manager(manager_user: User):
    token = create_access_token(
        {"user_id": manager_user.user_id, "sub": str(manager_user.email), "role": manager_user.role.value}
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def token_headers_customer(customer_user: User):
    token = create_access_token(
        {"user_id": customer_user.user_id, "sub": str(customer_user.email), "role": customer_user.role.value}
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def create_product_factory(db_session: AsyncSession):
    async def factory(**kwargs):
        from app.models import Product

        product = Product(**kwargs)
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product

    return factory
