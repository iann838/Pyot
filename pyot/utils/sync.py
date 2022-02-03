from typing import Awaitable, Callable, TypeVar
from functools import wraps
import asyncio


R = TypeVar("R")


def async_to_sync(func: Callable[..., Awaitable[R]]) -> Callable[..., R]:
    '''Wraps `asyncio.run` on an async function making it sync callable. Can be used as decorator @async_to_sync'''
    if not asyncio.iscoroutinefunction(func):
        raise TypeError(f"{func} is not a coroutine function")
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper
