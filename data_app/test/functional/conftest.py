import asyncio

import aiohttp
import pytest_asyncio

from src.core.config import settings


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


@pytest_asyncio.fixture(name="url_hash_service", scope="session")
async def url_service():
    yield f"http://{settings.app_host}:{settings.app_port}"
