import asyncio
import traceback
from typing import Any, Callable, List, Dict, Awaitable, TypeVar, Optional, Type

from pyot.utils.logging import Logger
from .exceptions import PyotException


LOGGER = Logger(__name__)

T = TypeVar('T')


class Item:

    def __init__(self, id, coro):
        self.id = id
        self.coro = coro


class Queue:
    '''A managed Queue on top of asyncio.Queue. This Queue is only usable as a context manager.'''
    queue: asyncio.Queue
    workers_num: int
    maxsize: int
    responses: Dict
    counter: int
    workers: List
    exception_handler: Callable[[Exception], Any]

    def __init__(self, workers: int = 25, maxsize: int = None, log_level: int = 0, exception_handler: Callable[[Exception], Any] = LOGGER.warning):
        if workers < 1: raise ValueError('Number of workers must be an integer greater than 0')
        self.workers_num = workers
        self.exception_handler = exception_handler
        if maxsize is None:
            self.maxsize = workers * 2
        else:
            self.maxsize = maxsize
        self.log_level = log_level

    async def worker(self, queue):
        while True:
            item: Item = await queue.get()
            try:
                res = await item.coro
                if res is not None:
                    self.responses[item.id] = res
            except Exception as e:
                self.exception_handler(traceback.format_exc())
            finally:
                queue.task_done()

    async def __aenter__(self) -> "Queue":
        self.queue = asyncio.Queue(maxsize=self.maxsize)
        self.responses = {}
        self.workers = []
        self.counter = 0
        for _ in range(self.workers_num):
            worker = asyncio.create_task(self.worker(self.queue))
            self.workers.append(worker)
        LOGGER.log(self.log_level, f"[Trace: Pyot Queue] Spawned {self.workers_num} workers")
        return self

    async def __aexit__(self, *args):
        await self.queue.join()
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
        LOGGER.log(self.log_level, f"[Trace: Pyot Queue] Joined {self.workers_num} workers")
        return

    async def put(self, coro: Awaitable, delay: float = 0):
        '''
        Put a coroutine object to the queue, if the queue is full, wait for availability.
        A delay may be provided if desired for execution balancing.
        '''
        if delay > 0:
            await asyncio.sleep(delay)
        if not asyncio.iscoroutine(coro):
            raise ValueError(f"[Trace: Pyot Queue] {str(coro)} is not a coroutine")
        await self.queue.put(Item(self.counter, coro))
        self.counter += 1

    async def join(self, class_of_t: Optional[Type[T]] = None) -> List[T]:
        '''
        Block until all items in the queue have been gotten and processed.
        Empty the collected responses and returns them.

        NoneType and Exceptions are not collected, order of the responses might not correspond the put order.
        '''
        await self.queue.join()
        response = [res[1] for res in sorted(self.responses.items())]
        self.responses = {}
        self.counter = 0
        return response
