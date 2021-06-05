from typing import Dict, Tuple, Any
import json

import aiohttp

from pyot.pipeline.handler import ErrorHandler
from pyot.pipeline.token import PipelineToken
from pyot.utils.logging import Logger

from .base import Store, StoreType


LOGGER = Logger(__name__)


class CloudLine(Store):
    '''Store that connects to an external pyot pipeline'''

    type = StoreType.SERVICE

    def __init__(self, game: str, location: str, target: str, error_handler: Dict[int, Tuple] = None, log_level: int = 0):
        self.target = target
        self.game = game
        self.location = location
        self.handler = ErrorHandler(error_handler, 800)
        self.log_level = log_level

    async def request(self, method: str, token: PipelineToken, session: aiohttp.ClientSession, body: Dict = None, **kwargs) -> Any:
        url = self.location
        error_token = self.handler.get_token()
        request_header = {"Pyot-Cloudline-Method": method.lower(), "Pyot-Cloudline-Target": self.target}
        request_body = {"token": token.dict(), "body": body}
        while error_token.allow():
            try:
                response = await session.request("POST", url=url, headers=request_header, json=request_body)
                LOGGER.log(self.log_level, f"[Trace: {self.game} > CloudLine] {method}: {token.value}")
            except Exception:
                response = None

            if response and response.status == 200:
                try:
                    res = await response.read()
                    return json.loads(res, encoding="utf-8")
                except json.decoder.JSONDecodeError:
                    return await response.text()

            code = response.status if response is not None else 408

            await error_token.consume(code, token.value)
