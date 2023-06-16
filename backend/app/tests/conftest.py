"""
Настрйоки для pytest
"""

import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.auth.db import get_async_session
from app.db.models import metadata
from app.core.config import settings
from app.main import app

# TODO: Переделать conftest как в fastapi-templates
# TODO: Автоматизировать создание test_db через фикстуру


DATABASE_URL_TEST = f"postgresql+asyncpg://" \
                    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASS}" \
                    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/" \
                    f"test_db"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test,
                                   class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
