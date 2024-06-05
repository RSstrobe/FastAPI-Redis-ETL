from redis.asyncio import Redis

from core.config import settings

redis: Redis = Redis(
    host=settings.redis.redis_host,
    port=settings.redis.redis_port,
    db=settings.redis.redis_database,
)


async def get_redis() -> Redis:
    return redis
