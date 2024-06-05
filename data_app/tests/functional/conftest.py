import asyncio

import aiohttp
import pytest_asyncio
from redis.asyncio import Redis

from tests.functional.core.config import test_settings


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="aiohttp_session", scope="session")
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name="url_service", scope="session")
async def url_service():
    yield f"http://{test_settings.app_host}:{test_settings.app_port}"


@pytest_asyncio.fixture(name="redis_client", scope="session")
async def redis_client():
    redis_client = Redis(
        host=test_settings.redis_host,
        port=test_settings.redis_port,
        db=test_settings.redis_database,
    )
    yield redis_client
    await redis_client.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def flush_redis(redis_client):
    await redis_client.flushall()


@pytest_asyncio.fixture(name="redis_read_data", scope="session")
def redis_read_data(redis_client):
    async def inner(key: str):
        data = await redis_client.get(str(key))
        if not data:
            return None

        return data

    return inner
