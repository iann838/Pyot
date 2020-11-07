import re
from datetime import datetime, timedelta
from typing import Mapping, Tuple, Dict, List, Any
from json import JSONDecodeError, loads
from logging import getLogger
import aiohttp
import asyncio

from pyot.core import exceptions as exc
from pyot.pipeline.token import PipelineToken, RequestToken
from pyot.pipeline.objects import StoreObject
from pyot.pipeline.handler import ErrorHandler

LOGGER = getLogger(__name__)


class DDragon(StoreObject):
    unique = True
    store_type = "SERVICE"

    def __init__(self, game: str, error_handling: Dict[int, Tuple] = None, version: str = 'latest', log_level: int = 10):
        handler = ErrorHandler()
        self._game = game
        self._handler_map = handler.create_handler(error_handling)
        self._endpoints = DDragonEndpoints(game, version)
        self._log_level = log_level
        self._last_updated = datetime.now()

    async def get(self, token: PipelineToken, session: aiohttp.ClientSession) -> Dict:
        url = await self._endpoints.resolve(token)
        request_token = RequestToken()
        while await request_token.run_or_raise():
            try:
                response = await session.request("GET", url)
                LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DDragon] GET: {self._log_template(token)}")
            except Exception:
                response = None

            if response and response.status == 200:
                try:
                    res = await response.read()
                    return loads(res, encoding="utf-8")
                except JSONDecodeError:
                    return await response.text()

            code = response.status if response is not None else 408
            try:
                how = self._handler_map[code]
            except KeyError:
                how = self._handler_map[800]
            await request_token.stream(code, how, self._log_template(token))


class DDragonEndpoints:
    _endpoints = {
        "lor": {
            "ddragon_lor_set_data": "/set{set}/{locale}/data/set{set}-{locale}.json"
        }
    }

    _base_url = "https://dd.b.pvp.net/{version}"

    def __init__(self, game, version):
        try:
            self.endpoints = self._endpoints[game]
            self._base_url = self._base_url.format(version=version)
        except KeyError as e:
            raise NotImplementedError(f"DDragon does not support '{e}' model")

    async def resolve(self, token: PipelineToken) -> str:
        try:
            base = self._base_url
            new_params = {"locale": token.server}
            new_params.update(token.params)
            url = self.endpoints[token.method].format(**new_params)
            return base + url
        except KeyError:
            raise exc.NotFindable
