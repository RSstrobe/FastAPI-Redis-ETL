import logging
from contextlib import asynccontextmanager

import uvicorn
from core.logger import LOGGING
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from api.v1.user_info import router as user_info_router

from core.config import settings
from db import redis_db


@asynccontextmanager
async def lifespan(application: FastAPI):
    redis_db.redis = Redis(
        host=settings.redis.redis_host,
        port=settings.redis.redis_port,
        db=settings.redis.redis_database,
    )
    yield
    await redis_db.redis.close()


app = FastAPI(
    title=settings.service_name,
    description="User info service",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router=user_info_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.backend.backend_host,
        port=settings.backend.backend_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
