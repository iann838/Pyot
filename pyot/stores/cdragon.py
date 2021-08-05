from typing import Tuple, Dict
import aiohttp

from pyot.pipeline.token import PipelineToken
from pyot.pipeline.handler import ErrorHandler
from pyot.endpoints.cdragon import CDragonEndpoint
from pyot.utils.parsers import safejson
from pyot.utils.logging import Logger
from pyot.utils.nullsafe import _

from .base import Store, StoreType


LOGGER = Logger(__name__)


class CDragon(Store):

    type = StoreType.SERVICE

    def __init__(self, game: str, error_handler: Dict[int, Tuple] = None, log_level: int = 0):
        self.game = game
        self.handler = ErrorHandler(error_handler, 800)
        self.endpoints = CDragonEndpoint(game)
        self.log_level = log_level

    async def get(self, token: PipelineToken, session: aiohttp.ClientSession, **kwargs) -> Dict:
        url = self.endpoints.resolve(token)
        error_token = self.handler.get_token()
        while error_token.allow():
            try:
                response = await session.request("GET", url)
                LOGGER.log(self.log_level, f"[Trace: {self.game} > CDragon] GET: {token.value}")
            except Exception:
                response = None

            status = _(response).status or 408
            if status == 200:
                return await response.json(encoding="utf-8", content_type=None, loads=safejson)
            await error_token.consume(status, token.value)
