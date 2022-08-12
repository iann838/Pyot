import functools
from typing import Awaitable, Callable, TypeVar
from functools import wraps
import inspect
import asyncio


R = TypeVar("R")


def async_to_sync(func: Callable[..., Awaitable[R]]) -> Callable[..., R]:
    '''Wraps `asyncio.run` on an async function converting it into a blocking function. Can be used as decorator @async_to_sync'''
    if not inspect.iscoroutinefunction(func):
        raise TypeError(f"{func} is not a coroutine function")
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


def sync_to_async(func: Callable[..., R]) -> Callable[..., Awaitable[R]]:
    '''Wraps `asyncio.get_event_loop().run_in_executor` on a blocking function converting it into a Future. Can be used as decorator @sync_to_async'''
    @wraps(func)
    async def wrapper(*args, **kwargs):
        new_func = functools.partial(func, *args, **kwargs)
        return await asyncio.get_event_loop().run_in_executor(None, new_func)
    return wrapper
