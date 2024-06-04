import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class _BaseSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class CommonSettings(_BaseSettings):
    service_name: str = Field(
        default="User info service",
        description="Название сервиса авторизации",
    )
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        description="Корень проекта",
    )
    debug_mode: bool = Field(
        default=False,
        description="Режим отладки сервиса авторизации",
    )


class RedisSettings(_BaseSettings): #TODO: redisDSN
    redis_host: str = Field(
        # default="redis_phone",
        description="Адрес хоста Redis для модуля авторизации",
    )
    redis_port: int = Field(
        # default=6379,
        description="Порт Redis для сервиса авторизации",
    )
    redis_database: str = Field(
        # default="0",
        description="База данных для хранения токенов",
    )
    redis_password: str = Field(
        # default="pass",
        description="Пароль от Redis",
    )
    ttl_redis: int = Field(
        # default=3600,
        description="Время хранения токенов",
    )


class BackendSettings(_BaseSettings):
    backend_host: str = Field(
        default="data_app",
        description="Адрес хоста сервиса авторизации",
    )
    backend_port: int = Field(
        default=8000,
        description="Порт сервиса авторизации",
    )


class Settings(CommonSettings):
    redis: RedisSettings = RedisSettings()
    backend: BackendSettings = BackendSettings()


settings = Settings()
