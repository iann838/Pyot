from typing import Awaitable, TypeVar
from functools import wraps
import asyncio

R = TypeVar("R")

def async_to_sync(func: Awaitable[R]) -> R:
    '''Wraps `asyncio.run` on an async function making it sync callable.'''
    if not asyncio.iscoroutinefunction(func):
        raise TypeError(f"{func} is not a coroutine function")
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper
