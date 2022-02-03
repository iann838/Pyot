from datetime import datetime
import asyncio

from .runners import loop_run


def timeit(func_or_coro, iters: int = 1, concurrent: bool = True):
    '''
    Measures the running time of a function or coroutine.
    Functions/Coroutines with arguments should be passed using `functools.partial`.
    `iters` may be passed to specify the amount of repeat executions.
    `concurrent` to allow concurrent running of coroutines.
    '''
    now = datetime.now()
    if asyncio.iscoroutinefunction(func_or_coro):
        if not concurrent:
            for _ in range(iters): loop_run(func_or_coro())
        else:
            loop_run(asyncio.gather(*[func_or_coro() for _ in range(iters)]))
    else:
        for _ in range(iters): func_or_coro()
    return str(datetime.now() - now)


async def atimeit(coro, iters: int = 1, concurrent: bool = True):
    '''
    Coroutine. measures the running time of a coroutine.

    Coroutines with arguments should be passed using `functools.partial`.
    `iters` may be passed to specify the amount of repeat executions.
    `concurrent` to allow concurrent running of coroutines.
    '''
    now = datetime.now()
    if concurrent:
        await asyncio.gather(*[coro() for _ in range(iters)])
        return str(datetime.now() - now)
    for _ in range(iters):
        await coro()
    return str(datetime.now() - now)
