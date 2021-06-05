from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from aiohttp.client_reqrep import ClientResponse

from pyot.utils.logging import Logger


LOGGER = Logger(__name__)


class LimiterToken:

    def __init__(self, server: str, method: str, epoch: float, sleep: float, allowed: List[str], pinging: List[Tuple[str, str, int]]) -> None:
        self.server = server
        self.method = method
        self.epoch = epoch
        self.sleep = sleep
        self.allowed = allowed
        self.pinging = pinging

    def allow(self):
        return self.sleep == 0


class BaseLimiter(ABC):

    def parse_headers(self, response: ClientResponse) -> Dict[str, List[List[int]]]:
        if response is None:
            return None
        headers = response.headers if hasattr(response, "headers") else None
        if headers is None:
            return None
        try:
            app_limit = [[int(val) for val in token.split(':')] for token in headers["X-App-Rate-Limit"].split(',')]
            app_count = [[int(val) for val in token.split(':')] for token in headers["X-App-Rate-Limit-Count"].split(',')]
            method_limit = [[int(val) for val in token.split(':')] for token in headers["X-Method-Rate-Limit"].split(',')]
            method_count = [[int(val) for val in token.split(':')] for token in headers["X-Method-Rate-Limit-Count"].split(',')]
            # if len(method_limit) == 1:
            #     method_limit.append(method_limit[0])
            # if len(method_count) == 1:
            #     method_count.append(method_count[0])
            return {
                "app_limit": app_limit,
                "app_count": app_count,
                "method_limit": method_limit,
                "method_count": method_count,
            }
        except KeyError:
            return None

    def parse_429(self, response: ClientResponse) -> Dict:
        if response is None:
            return None
        headers = response.headers if hasattr(response, "headers") else None
        if headers is None:
            return None
        return {
            "type": response.headers["X-Rate-Limit-Type"] if "X-Rate-Limit-Type" in response.headers else "service",
            "time": response.headers["Retry-After"] if "Retry-After" in response.headers else 1,
        }

    @abstractmethod
    def __init__(self, game: str, api_key: str, limiting_share: int = 1):
        self.game = game
        self.api_key = api_key
        self.limiting_share = limiting_share

    @abstractmethod
    async def get_token(self, server: str, method: str) -> LimiterToken:
        pass

    @abstractmethod
    async def sync_rates(self, token: LimiterToken, response: ClientResponse):
        pass

    @abstractmethod
    async def ping_fail(self, token: LimiterToken):
        pass

    @abstractmethod
    async def freeze_rates(self, token: LimiterToken, response: ClientResponse):
        pass
