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


class CDragonTransformers:
    _base_url = "https://raw.communitydragon.org/latest/"

    def __init__(self, locale):
        if locale.lower() == "en_us":
            self.locale = "default"
        else:
            self.locale = locale

    def url_assets(self, link: str) -> str:
        if link is None: return link
        link = link.lower()
        if len(link.split("/lol-game-data/assets/")) == 2:
            link = self._base_url+ f"plugins/rcp-be-lol-game-data/global/{self.locale}/" + link.split("/lol-game-data/assets/")[1]
        return link

    def start_k(self, string: str) -> str:
        if string is None: return string
        return string[1:] if string[0] == "k" else string

    def sanitize(self, string: str) -> str:
        if string is None: return string
        new_string = ""
        is_tag = False
        is_at = False
        tag = ""
        for s in string:
            if not is_tag and not is_at and s not in "<>@":
                new_string += s
            if s == "<":
                is_tag = True
            elif s == ">":
                is_tag = False
                if tag == "br" and len(new_string) > 0 and new_string[-1] != " ":
                    new_string += " "
                tag = ""
            elif s == "@" and not is_at:
                is_at = True
                new_string += "(?)"
            elif s == "@":
                is_at = False
            if is_tag and s not in "<>":
                tag += s
        return new_string
    


class CDragonEndpoints:
    _endpoints = {
        "lol": {
            "cdragon_champion_by_id": "/latest/plugins/rcp-be-lol-game-data/global/{locale}/v1/champions/{id}.json",
            "cdragon_item_full": "/latest/plugins/rcp-be-lol-game-data/global/{locale}/v1/items.json",
            "cdragon_rune_full": "/latest/plugins/rcp-be-lol-game-data/global/{locale}/v1/perks.json",
            "cdragon_spells_full": "/latest/plugins/rcp-be-lol-game-data/global/{locale}/v1/summoner-spells.json",
            "cdragon_profile_icon_full": "/latest/plugins/rcp-be-lol-game-data/global/{locale}/v1/profile-icons.json",
        }
    }

    _transformers = {
        "cdragon_champion_by_id": {
            "final": "id",
            "by_key": {},
            "by_name": {},
        }
    }

    _base_url = "https://raw.communitydragon.org"

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
            new_params = {"locale": token.server}
            new_params.update(token.params)
            url = self.endpoints[token.method].format(**new_params)
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
                    self._endpoints._transformers["cdragon_champion_by_id"]["by_key"][champ["alias"]] = champ["id"]
                    self._endpoints._transformers["cdragon_champion_by_id"]["by_name"][champ["name"]] = champ["id"]
            else:
                raise RuntimeError("[Trace: CDragon]: Store failed to initialize, "+
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

