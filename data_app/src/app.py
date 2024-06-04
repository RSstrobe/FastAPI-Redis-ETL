from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from api.v1.handlers import data_router
from deps import create_redis_repository


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_repo = create_redis_repository()
    yield
    await redis_repo.close_connection()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.service_name,
        description="User info service",
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(router=data_router)
    return app
