import asyncio
import sys

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from alembic import command
from alembic.config import Config
from app.dependencies import get_session
from app.entrypoints.fastapi_app import app
from tests.test_config import TEST_DATABASE_URL

if sys.platform == "darwin":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

# Setup test engine + session
engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")


# Override session dependency
async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


# Async HTTP client for FastAPI
@pytest_asyncio.fixture
async def async_client(apply_migrations):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
