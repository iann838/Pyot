from logging import getLogger
from typing import List, Coroutine
import aiohttp
import asyncio
import uuid
from pyot.pipeline import pipelines

LOGGER = getLogger(__name__)


class Queue:
    '''
    A managed Queue on top of asyncio.Queue. This Queue is only usable as a context manager.

    Unlike Gatherer, Queue has real workers that acts like consumers.
    A session is created and accessible on 'sid' attribute, the maxsize will default to workers * 2.
    Normally the queue object will be passed down to coroutines to give access to session id or queue methods. 
    '''
    session: aiohttp.ClientSession
    queue: asyncio.Queue
    workers_num: int
    maxsize: int
    responses: List
    workers: List
    sid: str

    def __init__(self, workers: int = 25, maxsize: int = None, log_level: int = 10):
        if workers < 1: raise RuntimeError('Number of workers must be an integer greater than 0')
        self.workers_num = workers
        if maxsize is None:
            self.maxsize = workers * 2
        else:
            self.maxsize = maxsize
        self.log_level = log_level
    
    async def worker(self, queue):
        while True:
            coro = await queue.get()
            try:
                res = await coro
                if res is not None:
                    self.responses.append(res)
            except Exception as e:
                LOGGER.warning(f"[Trace: Pyot Queue] WARNING: Unhandled exception '{e.__class__.__name__}: {e}' was raised and ignored")
            finally:
                queue.task_done()

    async def __aenter__(self) -> "Queue":
        self.queue = asyncio.Queue(maxsize=self.maxsize)
        self.responses = []
        self.workers = []
        for _ in range(self.workers_num):
            worker = asyncio.create_task(self.worker(self.queue))
            self.workers.append(worker)
        LOGGER.log(self.log_level, f"[Trace: Pyot Queue] Spawned {self.workers_num} workers")
        self.sid = uuid.uuid4()
        LOGGER.log(self.log_level, f"[Trace: Pyot Queue] Created session '{self.sid}'")
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        for pipeline in pipelines.values():
            pipeline.sessions[self.sid] = self.session
        return self

    async def __aexit__(self, *args):
        await self.queue.join()
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.is_joined = True
        LOGGER.log(self.log_level, f"[Trace: Pyot Queue] Joined {self.workers_num} workers")
        await self.session.close()
        LOGGER.log(self.log_level, f"[Trace: Pyot Queue] Closed session '{self.sid}'")
        for pipeline in pipelines.values():
            pipeline.sessions.pop(self.sid)
        return

    async def put(self, coro: Coroutine, delay: float = 0):
        '''
        Put a coroutine object to the queue, if the queue is full, wait for availability.
        A delay may be provided if desired for execution balancing.
        '''
        if delay > 0:
            await asyncio.sleep(delay)
        if not asyncio.iscoroutine(coro):
            raise RuntimeError(f"[Trace: Pyot Queue] {str(coro)} is not a coroutine")
        await self.queue.put(coro)

    async def join(self) -> List:
        '''
        Block until all items in the queue have been gotten and processed.
        Empty the collected responses and returns them.

        NoneType and Exceptions are not collected, order of the responses might not correspond the put order.
        '''
        await self.queue.join()
        res = self.responses
        self.responses = []
        return res
