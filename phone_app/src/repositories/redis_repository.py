import json
import logging

from fastapi import Depends
from redis.asyncio import Redis

from core.config import settings
from db.redis_db import get_redis
from repositories.base import BaseRepository

logger = logging.getLogger(__name__)

LIFETIME = settings.redis.ttl_redis


class RedisRepository(BaseRepository):
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get(self, key: str):
        try:
            data = await self.redis_client.get(str(key))
        except ConnectionError as e:
            data = None
            logger.error(e)

        if not data:
            return None
        return json.loads(data)

    async def set(self, key: str, value: str):
        try:
            await self.redis_client.set(key, value, ex=LIFETIME)
        except ConnectionError as e:
            logger.error(e)


async def get_redis_repo(redis_client: Redis = Depends(get_redis)):
    return RedisRepository(redis_client=redis_client)
