from .pipeline import PyotPipeline
from typing import List, Mapping, Any
import aiohttp
import asyncio
import uuid
import inspect

from logging import getLogger
LOGGER = getLogger(__name__)


class Registry:
    PIPELINES: Mapping[str, PyotPipeline] = {}
    GATHERER_SETTINGS: Mapping[str, Any] = {
        "workers": 200,
        "logs_enabled": True,
        "session_class": aiohttp.ClientSession,
        "cancel_on_raise": False,
    }

REGISTRY = Registry()


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

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return

    async def gather(self):
        """Awaitable, starts the scraping process and saves results to `responses`"""
        session_id = uuid.uuid4()
        if self.logs_enabled:
            LOGGER.warning(f"[Trace: Pyot Gatherer] Creating session '{session_id}', adding session id to statements ...")
        async with self.session_class() as session, asyncio.Semaphore(self.workers) as _:

            for pipeline in REGISTRY.PIPELINES.values():
                pipeline.sessions[session_id] = session


            for i in range(len(self.statements)):
                try:
                    self.statements[i] = asyncio.create_task(self.statements[i].set_session_id(session_id).get())
                except Exception:
                    raise RuntimeError(f"[Trace: Pyot Gatherer] Failed to add session id to statements at index {i}, "
                        "make sure that only Pyot objects are included and 'get()' is not passed on the statements")

            if self.cancel_on_raise:
                try:
                    self.responses = await asyncio.gather(*self.statements)
                except Exception as e:
                    for task in self.statements:
                        task.cancel()
                    if self.logs_enabled:
                        LOGGER.warning(f"[Trace: Pyot Gatherer] All statements of session '{session_id}' are cancelled due to exception: {e}")
                    raise
            else:
                self.responses = await asyncio.gather(*self.statements, return_exceptions=True)

            if self.logs_enabled:
                LOGGER.warning(f"[Trace: Pyot Gatherer] Closing session '{session_id}', cleaning up pipeline ...")
            for pipeline in REGISTRY.PIPELINES.values():
                pipeline.sessions.pop(session_id)


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

pipelines = REGISTRY.PIPELINES
