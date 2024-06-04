import logging

from redis.asyncio import Redis

from core.config import settings
from repositories.base import BaseRepository

logger = logging.getLogger(__name__)

LIFETIME = settings.redis.ttl_redis


class RedisRepository(BaseRepository):
    _instance: 'RedisRepository | None' = None

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get(self, key: str) -> bytes | None:
        try:
            data = await self.redis_client.get(str(key))
        except ConnectionError as e:
            data = None
            logger.error(e)

        return data

    async def set(self, key: str, value: str):
        try:
            await self.redis_client.set(key, value, ex=LIFETIME)
        except ConnectionError as e:
            logger.error(e)

    @classmethod
    def create_singleton(cls, **kw) -> 'RedisRepository':
        if cls._instance is None:
            cls._instance = cls(redis_client=kw.pop('redis_client'))
        return cls._instance

    def close_connection(self):
        self.redis_client.close()
