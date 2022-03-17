from functools import partial
from typing import Any, Mapping, Sequence, TypeVar, Callable, Awaitable
import asyncio


R = TypeVar("R")


def loop_run(coro: Awaitable[R]) -> R:
    '''Run the coroutine in the current event loop or a new one if `set_event_loop()` has not yet been called.'''
    return asyncio.get_event_loop().run_until_complete(coro)


async def thread_run(func: Callable[..., R], *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> R:
    '''Run a blocking function in a thread.'''
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))
