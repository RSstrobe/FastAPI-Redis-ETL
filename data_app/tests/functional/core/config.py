from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    redis_host: str = Field("localhost")
    redis_port: int = Field(6379)
    redis_database: int = Field(0)
    redis_password: str = Field("password")
    app_host: str = Field("127.0.0.1")
    app_port: int = Field(8080)


test_settings = TestSettings()
