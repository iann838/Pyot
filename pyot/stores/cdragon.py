from .__core__ import PyotStoreObject, PyotErrorHandler, PyotRequestToken
from ..core.pipeline import PyotPipelineToken
from ..core import exceptions as exc
from datetime import datetime, timedelta
from typing import Mapping, Tuple, Dict, List, Any
from json import JSONDecodeError
import aiohttp
import copy
import asyncio

from logging import getLogger
LOGGER = getLogger(__name__)


class CDragonEndpoints:
    _endpoints = {
        "lol": {
            "cdragon-champion-by-id": "/pbe/plugins/rcp-be-lol-game-data/global/default/v1/champions/{id}.json",
            "cdragon-item-by-id": "/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json",
        }
    }

    _transformers = {
        "cdragon-champion-by-id": {
            "final": "id",
            "by_key": {},
            "by_name": {},
        }
    }
    
    _base_url = "https://raw.communitydragon.org"

    def __init__(self, game):
        self.endpoints = self._endpoints[game]

    def transform_key(self, token: PyotPipelineToken):
        for method, tr in self._transformers.items():
            if token.method == method:
                if token.params.keys()[0] == tr["final"]:
                    return token
                token_ = copy.deepcopy(token)
                key = token_.params.keys()[0]
                val = token_.params[key]
                final_params = {}
                final_params[tr["final"]] = getattr(self, tr["by_"+key])[val]
                token_.params = final_params
                return token_
        return token

    async def resolve(self, token: PyotPipelineToken) -> str:
        try:
            base = self._base_url
            token_ = self.transform_key(token)
            url = self.endpoints[token_.method].format(**token_.params)
            return base + url
        except KeyError:
            raise exc.NotFound


class CDragon(PyotStoreObject):
    unique = True

    def __init__(self, game: str, error_handling: Dict[int, Tuple], logs_enabled: bool = True):
        handler = PyotErrorHandler()
        self._handler_map = handler.create_handler(error_handling)
        self._endpoints = CDragonEndpoints(game)
        self._logs_enabled = logs_enabled
        self._last_updated = datetime.now()
    
    async def initialize(self, reinit=False):
        url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/en_gb/v1/champion-summary.json"
        async with aiohttp.ClientSession() as session: # type: aiohttp.ClientSession
            try:
                if not reinit:
                    LOGGER.warning("[Trace: CDragon] Store initializing ...")
                else:
                    LOGGER.warning("[Trace: CDragon] Updating initialized data ...")
                response = await session.request("GET", url)
            except RuntimeError:
                raise RuntimeError(f"Pyot coroutines need to be executed inside PyotPipeline loop")
            if response and response.status == 200:
                dic = await response.json(encoding="utf-8")
                for champ in dic:
                    if champ["id"] == -1:
                        continue
                    self._endpoints._transformers["cdragon-champion-by-id"]["by_key"][champ["alias"]] = champ["id"]
                    self._endpoints._transformers["cdragon-champion-by-id"]["by_name"][champ["name"]] = champ["id"]
            else:
                raise RuntimeError("[Trace: CDragon]: Store failed to initialize, "+
                    f"cdragon raw core file call responded with status code {response.status}")

    async def get(self, token: PyotPipelineToken) -> Dict:
        if self._last_updated + timedelta(hours=3) < datetime.now():
            self._last_updated = datetime.now()
            await self.initialize(True)
        url = await self._endpoints.resolve(token)
        request_token = PyotRequestToken()
        async with aiohttp.ClientSession() as session: # type: aiohttp.ClientSession
            while await request_token.run_or_raise():
                try:
                    if self._logs_enabled:
                        LOGGER.warning(f"[Trace: CDragon] GET: {self._log_template(token)}")
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
                await request_token.stream(code, how)

