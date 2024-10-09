import logging  # noqa: I001
from collections.abc import AsyncGenerator, Generator
from unittest.mock import patch

import pytest
import pytest_asyncio
import uvloop
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.pool import NullPool

from tests.utils import load_env  # type: ignore # noqa: F401
from app import models  # type: ignore # noqa: F401
from app.config import app_settings
from app.database.base import Base
from app.database.context import session_ctx
from app.database.dependency import get_session
from app.database.engine import create_async_engine
from tests.utils.email import MockEmailService
from tests.utils.testcontainers import DbContainer, FixedAsyncRedisContainer, FixedPostgresContainer

logging.getLogger("faker").setLevel(logging.ERROR)

pytest_plugins = [
    "tests.fixtures.factories",
]


@pytest.fixture(scope="session")
def event_loop_policy() -> uvloop.EventLoopPolicy:
    return uvloop.EventLoopPolicy()


# All below fixtures are used for api tests


@pytest.fixture(scope="session")
def timescale_container() -> Generator[DbContainer, None, None]:
    container = FixedPostgresContainer("timescale/timescaledb:latest-pg15", driver="asyncpg")
    yield container.start()
    container.stop()


@pytest_asyncio.fixture(scope="session")  # type: ignore
async def redis_client() -> AsyncGenerator[Redis, None]:  # type: ignore
    with FixedAsyncRedisContainer("redis:7.2-alpine") as container:
        async_redis_client = await container.get_async_client(decode_responses=True)  # type: ignore
        yield async_redis_client


@pytest.fixture(scope="session")
def patch_redis_client(redis_client: Redis) -> Generator[None, None, None]:  # type: ignore
    with patch(
        "app.extension.redis.client.get_redis_client",
        return_value=redis_client,
    ):
        yield


@pytest.fixture(scope="session")
def patch_email_service() -> Generator[None, None, None]:
    with patch(
        "app.module.email.service.EmailService",
        return_value=MockEmailService,
    ):
        yield


@pytest_asyncio.fixture(scope="session")  # type: ignore
async def async_engine(timescale_container: DbContainer) -> AsyncEngine:
    return create_async_engine(timescale_container.get_connection_url(), poolclass=NullPool)


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def async_session(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine, expire_on_commit=False, autoflush=False) as session:
        yield session


@pytest_asyncio.fixture(scope="session")  # type: ignore
async def client(
    async_engine: AsyncEngine, patch_redis_client: None, patch_email_service: None
) -> AsyncGenerator[AsyncClient, None]:
    """Fixture to create a FastAPI test client."""

    from app.main import app

    # Initialize the database
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_session() -> AsyncGenerator[None, None]:
        async with AsyncSession(async_engine, expire_on_commit=False, autoflush=False) as session:
            token = session_ctx.set(session)
            try:
                async with session.begin():
                    yield
            finally:
                session_ctx.reset(token)

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url=f"http://localhost{app_settings.API_PREFIX}",  # Using localhost for cookie testing
    ) as client:
        yield client
