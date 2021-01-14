from functools import wraps
import asyncio


def async_to_sync(func):
    if not asyncio.iscoroutinefunction(func):
        raise TypeError(f"{func} is not a coroutine function")
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper
