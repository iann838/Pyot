from typing import Mapping, Dict, Any, Union
import asyncio
import aiohttp
import requests

from pyot.pipeline.token import PipelineToken
from pyot.pipeline.handler import ErrorHandler
from pyot.endpoints.riotapi import RiotAPIEndpoint
from pyot.limiters.base import BaseLimiter
from pyot.utils.importlib import import_class
from pyot.utils.nullsafe import null_safe
from pyot.utils.parsers import json_safe
from pyot.utils.runners import thread_run
from pyot.utils.logging import Logger

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
        # Commented since Pyot 5: The issue was only seen on match-v4 timeline, now when it's gone, let's see.
        # request_manager = RiotAPIRequestManager(method=method, url=self.endpoints.resolve(token), headers={"X-Riot-Token": self.api_key}, json=body)
        while error_token.allow():
            limit_token = await self.rate_limiter.get_token(token.server, token.parent)
            if not limit_token.allow():
                await asyncio.sleep(limit_token.sleep)
                # await self.rate_limiter.ping_fail(limit_token) # handled
                continue
            # print(limit_token.sleep, url)
            try:
                # await request_manager.execute(session)
                # await request_manager.validate()
                # response = request_manager.response
                response = await session.request(method=method, url=url, headers={"X-Riot-Token": self.api_key}, json=body)
                LOGGER.log(self.log_level, f"[Trace: {self.game} > RiotAPI] {method}: {token.value}")
            except Exception:
                response = None

            await self.rate_limiter.sync_rates(limit_token, response)
            status = null_safe(response).status or 408
            if status == 200:
                return await response.json(encoding="utf-8", content_type=None, loads=json_safe)
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


class RiotAPIRequestManager:
    """Manages Riot API requests because aiohttp is not able to decrypt / read the response in very rare cases."""

    response: Union[aiohttp.ClientResponse, requests.Response]

    def __init__(self, method: str, url: str, headers: Dict, json: Dict) -> None:
        self.method = method
        self.url = url
        self.headers = headers
        self.json = json
        self.decode_error = False

    async def execute(self, session: aiohttp.ClientSession) -> None:
        if self.decode_error:
            response = await thread_run(requests.request, method=self.method, url=self.url, headers=self.headers, json=self.json)
            response.status = response.status_code
        else:
            response = await session.request(method=self.method, url=self.url, headers=self.headers, json=self.json)
        self.response = response

    async def validate(self):
        try:
            if self.decode_error:
                return
            await asyncio.wait_for(self.response.read(), timeout=5)
        except asyncio.TimeoutError:
            self.decode_error = True
            self.response.status = 602
