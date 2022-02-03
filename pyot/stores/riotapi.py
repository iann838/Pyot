from typing import Mapping, Dict, Any
import asyncio
import aiohttp

from pyot.pipeline.token import PipelineToken
from pyot.pipeline.handler import ErrorHandler
from pyot.endpoints.riotapi import RiotAPIEndpoint
from pyot.limiters.base import BaseLimiter
from pyot.utils.importlib import import_class
from pyot.utils.parsers import safejson
from pyot.utils.logging import Logger
from pyot.utils.nullsafe import _

from .base import Store, StoreType


LOGGER = Logger(__name__)


class RiotAPI(Store):

    type = StoreType.SERVICE

    def __init__(self, game: str, api_key: str, rate_limiter: Mapping[str, str] = None, error_handler: Mapping[int, Any] = None, log_level: int = 0, silence_429: bool = False):
        self.game = game
        self.api_key = api_key
        self.endpoints = RiotAPIEndpoint(game)
        self.handler = ErrorHandler(error_handler, 800)
        self.rate_limiter = self.create_rate_limiter(rate_limiter or {})
        self.log_level = log_level
        self.silence_429 = silence_429

    async def request(self, method: str, token: PipelineToken, body: Dict = None, session: aiohttp.ClientSession = None, **kwargs) -> Dict:
        url = self.endpoints.resolve(token)
        error_token = self.handler.get_token()
        while error_token.allow():
            limit_token = await self.rate_limiter.get_token(token.server, token.parent)
            if not limit_token.allow():
                await asyncio.sleep(limit_token.sleep)
                continue
            try:
                response = await session.request(method=method, url=url, headers={"X-Riot-Token": self.api_key}, json=body)
                LOGGER.log(self.log_level, f"[Trace: {self.game} > RiotAPI] {method}: {token.value}")
            except Exception:
                response = None

            await self.rate_limiter.sync_rates(limit_token, response)
            status = _(response).status or 408
            if status == 200:
                return await response.json(encoding="utf-8", content_type=None, loads=safejson)
            if status == 429:
                headers = await self.rate_limiter.freeze_rates(limit_token, response)
                if headers["type"] != "service" and not self.silence_429:
                    LOGGER.warning(f"[Trace: {self.game} > RiotAPI] WARN: Non-service 429 responded, interrupt tasks if mass 429s are being returned. Origin: {token.value}")
            await error_token.consume(status, token.value)

    def create_rate_limiter(self, dic: Dict[str, Any]) -> BaseLimiter:
        config = {key.lower(): val for (key, val) in dic.items()}
        try:
            limiter = import_class(config.pop("backend"))
        except KeyError:
            limiter = import_class('pyot.limiters.memory.MemoryLimiter')
        config["game"] = self.game
        config["api_key"] = self.api_key
        return limiter(**config)
