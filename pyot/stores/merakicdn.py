from datetime import datetime, timedelta
from typing import Mapping, Tuple, Dict, List, Any
from json import JSONDecodeError
from logging import getLogger
import aiohttp
import asyncio

from pyot.pipeline.objects import StoreObject
from pyot.pipeline.handler import ErrorHandler
from pyot.pipeline.token import PipelineToken, RequestToken
from pyot.core import exceptions as exc

LOGGER = getLogger(__name__)


class MerakiCDN(StoreObject):
    unique = True
    store_type = "SERVICE"

    def __init__(self, game: str, error_handling: Dict[int, Tuple] = None, log_level: int = 10):
        handler = ErrorHandler()
        self._game = game
        self._handler_map = handler.create_handler(error_handling)
        self._endpoints = MerakiCDNEndpoints(game)
        self._log_level = log_level
        self._last_updated = datetime.now()

    async def get(self, token: PipelineToken, session: aiohttp.ClientSession) -> Dict:
        url = await self._endpoints.resolve(token)
        request_token = RequestToken()
        while await request_token.run_or_raise():
            try:
                response = await session.request("GET", url)
                LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > MerakiCDN] GET: {self._log_template(token)}")
            except Exception:
                response = None

            if response and response.status == 200:
                try:
                    return await response.json(encoding="utf-8")
                except JSONDecodeError:
                    return await response.text()

            code = response.status if response is not None else 408
            try:
                how = self._handler_map[code]
            except KeyError:
                how = self._handler_map[800]
            await request_token.stream(code, how, self._log_template(token))


class MerakiCDNEndpoints:
    _endpoints = {
        "lol": {
            "meraki_champion_by_key": "/lol/resources/latest/en-US/champions/{key}.json",
            "meraki_item_by_id": "/lol/resources/latest/en-US/items/{id}.json"
        }
    }

    _base_url = "https://cdn.merakianalytics.com/riot"

    def __init__(self, game):
        try:
            self.endpoints = self._endpoints[game]
        except KeyError as e:
            raise NotImplementedError(f"MerakiCDN does not support '{e}' model")

    async def resolve(self, token: PipelineToken) -> str:
        try:
            base = self._base_url
            url = self.endpoints[token.method].format(**token.params)
            return base + url
        except KeyError:
            raise exc.NotFindable
