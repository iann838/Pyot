from .__core__ import PyotStoreObject, PyotErrorHandler, PyotRequestToken
from ..core.pipeline import PyotPipelineToken
from ..core import exceptions as exc
from datetime import datetime, timedelta
from typing import Mapping, Tuple, Dict, List, Any
from json import JSONDecodeError
import aiohttp
import asyncio

from logging import getLogger
LOGGER = getLogger(__name__)


class MerakiCDNEndpoints:
    _endpoints = {
        "lol": {
            "meraki_champion_by_key": "/lol/resources/latest/en-US/champions/{key}.json",
            "meraki_item_by_id": "/lol/resources/latest/en-US/items/{id}.json"
        }
    }

    _transformers = {
        "meraki_champion_by_key": {
            "final": "key",
            "by_id": {},
            "by_name": {},
        }
    }

    _base_url = "https://cdn.merakianalytics.com/riot"

    def __init__(self, game):
        self.endpoints = self._endpoints[game]

    def transform_key(self, method: str, key: str, content: str):
        for alias, tr in self._transformers.items():
            if alias == method:
                if tr["final"] == key:
                    return content
                return tr["by_"+key][content]
        return content

    async def resolve(self, token: PyotPipelineToken) -> str:
        try:
            base = self._base_url
            url = self.endpoints[token.method].format(**token.params)
            return base + url
        except KeyError:
            raise exc.NotFound


class MerakiCDN(PyotStoreObject):
    unique = True

    def __init__(self, game: str, error_handling: Dict[int, Tuple] = None, logs_enabled: bool = True):
        handler = PyotErrorHandler()
        if game != "lol":
            raise NotImplementedError("MerakiCDN only supports the LOL model")
        self._game = game
        self._handler_map = handler.create_handler(error_handling)
        self._endpoints = MerakiCDNEndpoints(game)
        self._logs_enabled = logs_enabled
        self._last_updated = datetime.now()
    
    async def initialize(self, reinit=False):
        url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/en_gb/v1/champion-summary.json"
        async with aiohttp.ClientSession() as session: # type: aiohttp.ClientSession
            try:
                if not reinit:
                    LOGGER.warning(f"[Trace: {self._game.upper()} > MerakiCDN] Store initializing ...")
                else:
                    LOGGER.warning(f"[Trace: {self._game.upper()} > MerakiCDN] Updating initialized data ...")
                response = await session.request("GET", url)
            except RuntimeError:
                raise RuntimeError(f"Pyot coroutines need to be executed inside PyotPipeline loop")
            if response and response.status == 200:
                dic = await response.json(encoding="utf-8")
                for champ in dic:
                    if champ["id"] == -1:
                        continue
                    self._endpoints._transformers["meraki_champion_by_key"]["by_id"][champ["id"]] = champ["alias"]
                    self._endpoints._transformers["meraki_champion_by_key"]["by_name"][champ["name"]] = champ["alias"]
            else:
                raise RuntimeError(f"[Trace: {self._game.upper()} > MerakiCDN]: Store failed to initialize, "+
                    f"cdragon raw core file call responded with status code {response.status}")

    async def get(self, token: PyotPipelineToken, session: aiohttp.ClientSession) -> Dict:
        if self._last_updated + timedelta(hours=3) < datetime.now():
            self._last_updated = datetime.now()
            await self.initialize(True)
        url = await self._endpoints.resolve(token)
        request_token = PyotRequestToken()
        while await request_token.run_or_raise():
            try:
                if self._logs_enabled:
                    LOGGER.warning(f"[Trace: {self._game.upper()} > MerakiCDN] GET: {self._log_template(token)}")
                response = await session.request("GET", url)
            except RuntimeError:
                raise RuntimeError(f"Pyot coroutines need to be executed inside PyotPipeline loop")
            except Exception:
                response = None

            if response and response.status == 200:
                try:
                    return await response.json(encoding="utf-8")
                except JSONDecodeError:
                    return await response.text()

            code = response.status if response is not None else 408
            how = self._handler_map[code] if self._handler_map[code] else self._handler_map[888]
            await request_token.stream(code, how, self._log_template(token))

