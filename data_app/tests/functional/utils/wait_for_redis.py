import os
from redis import Redis
from redis.exceptions import ConnectionError

from backoff import backoff


@backoff(connect_exception=ConnectionError)
def pinging_redis(redis_client: Redis) -> bool:
    return redis_client.ping()


if __name__ == "__main__":
    client = Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        db=os.getenv("REDIS_DATABASE"),
    )
    pinging_redis(redis_client=client)