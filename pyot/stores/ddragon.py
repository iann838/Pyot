from typing import Tuple, Dict
import aiohttp

from pyot.pipeline.token import PipelineToken
from pyot.pipeline.handler import ErrorHandler
from pyot.endpoints.ddragon import DDragonEndpoint
from pyot.utils.nullsafe import nullsafe
from pyot.utils.parsers import safejson
from pyot.utils.logging import Logger

from .base import Store, StoreType


LOGGER = Logger(__name__)


class DDragon(Store):

    type = StoreType.SERVICE

    def __init__(self, game: str, error_handler: Dict[int, Tuple] = None, log_level: int = 0):
        self.game = game
        self.handler = ErrorHandler(error_handler, 800)
        self.endpoints = DDragonEndpoint(game)
        self.log_level = log_level

    async def get(self, token: PipelineToken, session: aiohttp.ClientSession, **kwargs) -> Dict:
        url = self.endpoints.resolve(token)
        error_token = self.handler.get_token()
        while error_token.allow():
            try:
                response = await session.request("GET", url)
                LOGGER.log(self.log_level, f"[Trace: {self.game} > DDragon] GET: {token.value}")
            except Exception:
                response = None

            status = nullsafe(response).status or 408
            if status == 200:
                return await response.json(encoding="utf-8", content_type=None, loads=safejson)
            await error_token.consume(status, token.value)


# class DDragonEndpoints:
#     all_endpoints = {
#         "lor": {
#             "ddragon_lor_set_data": "/set{set}/{locale}/data/set{set}-{locale}.json"
#         }
#     }

#     _base_url = "https://dd.b.pvp.net/{version}"

#     def __init__(self, game, version):
#         try:
#             self.endpoints = self.all_endpoints[game]
#             self._base_url = self._base_url.format(version=version)
#         except KeyError as e:
#             raise NotImplementedError(f"DDragon does not support '{e}' model") from e

#     async def resolve(self, token: PipelineToken) -> str:
#         try:
#             base = self._base_url
#             new_params = {"locale": token.server}
#             new_params.update(token.params)
#             url = self.endpoints[token.method].format(**new_params)
#             return base + url
#         except KeyError as e:
#             raise exc.NotFindable from e
