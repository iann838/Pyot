from .__core__ import REGISTRY
from typing import Any, List
import aiohttp
import asyncio
import uuid


from logging import getLogger
LOGGER = getLogger(__name__)


class Gatherer:
    workers: int
    session_class: Any
    logs_enabled: bool
    cancel_on_raise: bool
    statements: List
    responses: List

    def __init__(self, workers: int = REGISTRY.GATHERER_SETTINGS["workers"], session_class: Any = REGISTRY.GATHERER_SETTINGS["session_class"],
        logs_enabled: bool = REGISTRY.GATHERER_SETTINGS["logs_enabled"], cancel_on_raise: bool = REGISTRY.GATHERER_SETTINGS["cancel_on_raise"]):
        """
        Scraper that wraps asyncio.gather, automatically create a session that 
        is reused across the statements provided to get data even faster
        """
        self.workers = workers
        self.session_class = session_class
        self.cancel_on_raise = cancel_on_raise
        self.logs_enabled = logs_enabled
        self.statements = []

    async def __aenter__(self):
        self.session_id = uuid.uuid4()
        if self.logs_enabled:
            LOGGER.warning(f"[Trace: Pyot Gatherer] Creating session '{self.session_id}', adding session id to statements ...")
        self.session = self.session_class(connector=aiohttp.TCPConnector(verify_ssl=False, limit=self.workers))
        for pipeline in REGISTRY.PIPELINES.values():
            pipeline.sessions[self.session_id] = self.session
        return self

    async def __aexit__(self, *args):
        if self.logs_enabled:
            LOGGER.warning(f"[Trace: Pyot Gatherer] Closing session '{self.session_id}', cleaning up pipeline ...")
        await self.session.close()
        for pipeline in REGISTRY.PIPELINES.values():
            pipeline.sessions.pop(self.session_id)
        return

    async def gather(self):
        """Awaitable, starts the scraping process and saves results to `responses`"""
        for i in range(len(self.statements)):
            try:
                self.statements[i] = self.statements[i].set_session_id(self.session_id).get
            except Exception:
                raise RuntimeError(f"[Trace: Pyot Gatherer] Failed to add session id to statements at index {i}, "
                    "make sure that only Pyot objects are included and 'get()' is not passed on the statements")

        try:
            self.responses = []
            splits = int(len(self.statements)/self.workers)+1
            for s in range(splits):
                bucket = [asyncio.create_task(st()) for st in self.statements[s*self.workers:(s+1)*self.workers if s+1 < splits else -1]]
                self.responses.extend(await asyncio.gather(*bucket, return_exceptions=False if self.cancel_on_raise else True))
        except Exception as e:
            for task in bucket:
                task.cancel()
            if self.logs_enabled:
                LOGGER.warning(f"[Trace: Pyot Gatherer] All statements of session '{self.session_id}' are cancelled due to exception: {e}")
            raise