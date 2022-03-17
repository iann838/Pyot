from typing import Awaitable, Callable, TypeVar
from functools import wraps
import asyncio

from .runners import thread_run


R = TypeVar("R")


def async_to_sync(func: Callable[..., Awaitable[R]]) -> Callable[..., R]:
    '''Wraps `asyncio.run` on an async function converting to sync callable. Can be used as decorator @async_to_sync'''
    if not asyncio.iscoroutinefunction(func):
        raise TypeError(f"{func} is not a coroutine function")
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


def sync_to_async(func: Callable[..., R]) -> Callable[..., Awaitable[R]]:
    '''Wraps `thread_run` on a blocking function converting to async by running in a thread. Can be used as decorator @sync_to_async'''
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await thread_run(func, *args, **kwargs)
    return wrapper
