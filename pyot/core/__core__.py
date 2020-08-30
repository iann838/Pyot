from .pipeline import PyotPipeline
from typing import Mapping, Any
import aiohttp
import asyncio


class Registry:
    PIPELINES: Mapping[str, PyotPipeline] = {}
    GATHERER_SETTINGS: Mapping[str, Any] = {
        "workers": 30,
        "logs_enabled": True,
        "session_class": aiohttp.ClientSession,
        "cancel_on_raise": False,
    }


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


REGISTRY = Registry()
pipelines = REGISTRY.PIPELINES
