from datetime import datetime, timedelta
from pyot.utils import SealLock
from typing import Any
from collections import defaultdict
import pytz

from .core import LimitToken, BaseLimiter
from pyot.utils import MultiDefaultDict


class MemoryLimiter(BaseLimiter):
    '''
    In Memory Riot Rate Limiter, unsuitable for multiprocessing.
    '''

    def __init__(self, game: str, api_key: str, limiting_share: int = 1):
        if limiting_share > 1 or limiting_share < 0: raise AttributeError('Limiting share must be a float between 0 and 1')
        yesterday = datetime.now(pytz.utc) - timedelta(days=1)
        self._game = game
        self._api_key = api_key
        self._lock = SealLock()
        self._limiting_share = limiting_share
        self._application_rates = MultiDefaultDict(lambda: [[None, 1, 20, 1],[None, 1, 100, 120]])
        self._application_times = MultiDefaultDict(lambda: [yesterday, yesterday])
        self._application_backoffs = defaultdict(lambda: yesterday)
        self._methods_rates = MultiDefaultDict(lambda: [[None, 1, 10, 60], [None, 1, 10, 60]])
        self._methods_times = MultiDefaultDict(lambda: [yesterday, yesterday])
        self._methods_backoffs = defaultdict(lambda: yesterday)
        self._methods_bucket = defaultdict(lambda: 0)
        self._application_bucket = defaultdict(lambda: 0)

        # Rates are recorded as [minumum_call_backed, current_call_passed, max_call_allowed, time_span]

    async def get_limit_token(self, server: str, method: str) -> LimitToken:
        async with self._lock:
            return await super().get_limit_token(server, method)

    async def put_stream(self, fetched: dict, server: str, method: str, token: LimitToken):
        async with self._lock:
            await super().put_stream(fetched, server, method, token)

    async def inmediate_backoff(self, seconds: int, type_: str, server: str, method: str = None):
        async with self._lock:
            await super().inmediate_backoff(seconds, type_, server, method)
