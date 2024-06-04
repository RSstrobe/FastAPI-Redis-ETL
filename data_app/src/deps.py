from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from starlette.requests import Request

from core.config import settings
from repositories.redis_repository import RedisRepository
from services.user_info_service import UserinfoService


def create_redis_client(
        *,
        host=settings.redis.redis_host,
        port=settings.redis.redis_port,
        db=settings.redis.redis_database
) -> Redis:
    redis = Redis(host=host, port=port, db=db)
    return redis


def create_redis_repository(redis_client=create_redis_client()):
    return RedisRepository.create_singleton(redis_client=redis_client)


def create_redis_repository_dependency(_: Request):
    return create_redis_repository()


RedisRepositoryType = Annotated[RedisRepository, Depends(create_redis_repository_dependency)]


def create_user_info_service(ui_repo: RedisRepositoryType):
    return UserinfoService(ui_repo=ui_repo)


UserDataService = Annotated[UserinfoService, Depends(create_user_info_service)]
