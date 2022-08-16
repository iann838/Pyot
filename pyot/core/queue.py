import asyncio
import inspect
import sys
import traceback
from types import TracebackType
from typing import Any, Callable, List, Dict, Awaitable, TypeVar, Optional, Type

from pyot.utils.logging import LazyLogger


LOGGER = LazyLogger(__name__)

T = TypeVar('T')

ExceptionHandlerFunction = Callable[[Type[BaseException], BaseException, TracebackType], Any]


class QueueItem:

    def __init__(self, id, coro):
        self.id = id
        self.coro = coro


class Queue:
    '''A managed Queue on top of asyncio.Queue. This Queue is only usable as a context manager.'''
    _id_counter: int
    _queue: asyncio.Queue

    workers: int
    maxsize: int
    responses: Dict
    worker_tasks: List[asyncio.Task]
    exception_handler: Callable[[Exception], Any]

    def __init__(self, workers: int = 25, maxsize: int = None, log_level: int = 0, exception_handler: ExceptionHandlerFunction = traceback.print_exception):
        if workers < 1: raise ValueError('Number of workers must be an integer greater than 0')
        self.workers = workers
        self.exception_handler = exception_handler
        if maxsize is None:
            self.maxsize = workers * 2
        else:
            self.maxsize = maxsize
        self.log_level = log_level

    async def worker(self, queue: asyncio.Queue):
        while True:
            item: QueueItem = await queue.get()
            try:
                res = await item.coro
                if res is not None:
                    self.responses[item.id] = res
            except Exception:
                one, two, three = sys.exc_info()
                self.exception_handler(one, two, three)
            finally:
                queue.task_done()

    async def __aenter__(self) -> "Queue":
        self._queue = asyncio.Queue(maxsize=self.maxsize)
        self.responses = {}
        self.worker_tasks = []
        self._id_counter = 0
        for _ in range(self.workers):
            worker = asyncio.create_task(self.worker(self._queue))
            self.worker_tasks.append(worker)
        LOGGER.log(self.log_level, f"[pyot.core.queue:Queue] Spawned {self.workers} workers")
        return self

    async def __aexit__(self, *args):
        await self._queue.join()
        for worker in self.worker_tasks:
            worker.cancel()
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        LOGGER.log(self.log_level, f"[pyot.core.queue:Queue] Joined {self.workers} workers")

    async def put(self, coro: Awaitable, delay: float = 0):
        '''
        Put a coroutine object to the queue, if the queue is full, wait for availability.
        A delay may be provided if desired for execution balancing.
        '''
        if delay > 0:
            await asyncio.sleep(delay)
        if not inspect.isawaitable(coro):
            raise ValueError(f"{str(coro)} is not awaitable")
        await self._queue.put(QueueItem(self._id_counter, coro))
        self._id_counter += 1

    async def join(self, class_of_t: Optional[Type[T]] = None) -> List[T]:
        '''
        Block until all items in the queue have been gotten and processed.
        Empty the collected responses and returns them.

        `None` and `Exception` responses are not collected, order of the responses might not correspond the put order.
        '''
        await self._queue.join()
        response = [res[1] for res in sorted(self.responses.items())]
        self.responses = {}
        self._id_counter = 0
        return response
