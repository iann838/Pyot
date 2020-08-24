from typing import List
import aiohttp
import asyncio
from .pipeline import PyotPipeline

from logging import getLogger
LOGGER = getLogger(__name__)


class Registry:
    PYOT_PIPELINES: List[PyotPipeline] = []
registry = Registry()



class Scraper:
    responses: List
    semaphore: int
    statements: List

    def __init__(self, semaphore: int = 10000, statements: List = []):
        """
        Scraper that wraps asyncio.gather, automatically create a session that 
        is reused across the statements provided to get data even faster
        """
        self.semaphore = semaphore
        self.statements = statements

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return

    async def scrape(self):
        """Awaitable, starts the scraping process and saves results to `responses`"""
        LOGGER.warning("[Trace: PyotScraper] Creating session and semaphore ...")
        async with aiohttp.ClientSession() as session, asyncio.Semaphore(self.semaphore) as _:
            for pipeline in registry.PYOT_PIPELINES:
                pipeline.session = session
            
            self.responses = await asyncio.gather(*self.statements)

            LOGGER.warning("[Trace: PyotScraper] Cleaning up session, waiting to exit ...")
            for pipeline in registry.PYOT_PIPELINES:
                pipeline.hold = True
                await asyncio.sleep(1)
                pipeline.session = None
                pipeline.hold = False


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)
