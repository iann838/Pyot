from typing import Any, List
from pyot.pipeline import pipelines
import aiohttp
import asyncio
import uuid


from logging import getLogger
LOGGER = getLogger(__name__)


class Gatherer:
    '''
    Scraper that wraps asyncio.gather, automatically create a session that
    is reused across the statements provided to get data even faster.

    For executing mass non-pyot coroutines, please use Queue instead.
    Unlike Queue, workers are fake workers, they only represent the size of the chunk to gather.
    '''
    workers: int
    session_class: Any
    log_level: int
    cancel_on_raise: bool
    statements: List
    responses: List

    def __init__(self, workers: int = 25, log_level: int = 10, cancel_on_raise: bool = False):
        self.workers = workers
        self.cancel_on_raise = cancel_on_raise
        self.log_level = log_level
        self.statements = []

    async def __aenter__(self) -> "Gatherer":
        self.session_id = uuid.uuid4()
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, limit=self.workers))
        for pipeline in pipelines.values():
            pipeline.sessions[self.session_id] = self.session
        LOGGER.log(self.log_level, f"[Trace: Pyot Gatherer] Created session '{self.session_id}'")
        return self

    async def __aexit__(self, *args):
        await self.session.close()
        for pipeline in pipelines.values():
            pipeline.sessions.pop(self.session_id)
        LOGGER.log(self.log_level, f"[Trace: Pyot Gatherer] Closed session '{self.session_id}'")
        return

    async def gather(self):
        '''Awaitable, starts the scraping process and saves results to `responses`.
        
        Gatherings are done by chunks, the size of the chunk is determined by the number of workers.
        '''
        for i in range(len(self.statements)):
            try:
                self.statements[i] = self.statements[i].get
            except Exception:
                raise RuntimeError(f"[Trace: Pyot Gatherer] Failed to add session id to statements at index {i}, "
                    "make sure that only Pyot objects are included and 'get()' is not passed on the statements")

        try:
            self.responses = []
            splits = int(len(self.statements)/self.workers)+1
            for s in range(splits):
                bucket = []
                for st in self.statements[s*self.workers:(s+1)*self.workers if s+1 < splits else None]:
                    bucket.append(asyncio.create_task(st(sid=self.session_id)))
                    await asyncio.sleep(0.01)
                self.responses.extend(await asyncio.gather(*bucket, return_exceptions=False if self.cancel_on_raise else True))
            return self.responses
        except Exception as e:
            for task in bucket:
                task.cancel()
            LOGGER.warning(f"[Trace: Pyot Gatherer] All statements of session '{self.session_id}' are cancelled due to exception: {e}")
            raise
