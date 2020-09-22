from datetime import datetime, timedelta
from asyncio import iscoroutine
from pyot.utils import loop_run


def timeit(func_or_coro, iters: int = 1):
    '''
    Measures the running time of a function or coroutine.
    Functions with arguments should be passed using `functools.partial`.
    `iters` may be passed to specify the amount of repeat executions.
    '''
    now = datetime.now()
    if iscoroutine(func_or_coro):
        [loop_run(func_or_coro)]*iters
    else:
        [func_or_coro()]*iters
    return str(datetime.now() - now)


async def atimeit(coro, iters: int = 1):
    '''
    Awaitable, measures the running time of a coroutine.
    `iters` may be passed to specify the amount of repeat executions.
    '''
    now = datetime.now()
    [await coro]*iters
    return str(datetime.now() - now)
