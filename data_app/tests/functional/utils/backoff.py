import time
from functools import wraps


def backoff(
        connect_exception: any,
        attempts: int = 10,
        start_sleep_time: float = 0.1,
        factor: int = 2,
        border_sleep_time: int = 10,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sleep_time = start_sleep_time
            for _ in range(attempts):
                result = func(*args, **kwargs)
                if result:
                    return None
                sleep_time = min(sleep_time * 2 ** factor, border_sleep_time)
                time.sleep(sleep_time)

            raise connect_exception(message="Service is not available")

        return wrapper

    return decorator
