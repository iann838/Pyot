from typing import Any, List
from logging import getLogger
from functools import partial
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.parser import parse
import asyncio
import pickle
import pytz
import redis

from pyot.utils import RedisLock, RedisDefaultDict, SealLock, pytify, bytify, fast_copy
from .core import LimitToken, BaseLimiter

LOGGER = getLogger(__name__)


class RedisLimiter(BaseLimiter):
    '''
    Riot Rate Limiter based on Redis, suitable for multiprocessing.
    '''

    def __init__(self, game: str, api_key: str, limiting_share = 1, host='127.0.0.1', port=6379, db=0, *args, **kwargs):
        if limiting_share > 1 or limiting_share < 0: raise AttributeError('Limiting share must be a float between 0 and 1')
        yesterday = datetime.now(pytz.utc) - timedelta(days=1)
        self._game = game
        self._api_key = api_key
        self._pool = redis.ConnectionPool(host=host, port=port, db=db, *args, **kwargs)
        self._redis = redis.Redis(connection_pool=self._pool)
        self._lock = lambda name: RedisLock(self._redis, name)
        self._seal = SealLock()
        self._limiting_share = limiting_share
        self._methods_backoffs = defaultdict(lambda: yesterday)
        self._application_backoffs = defaultdict(lambda: yesterday)
        self._methods_bucket = defaultdict(lambda: 0)
        self._application_bucket = defaultdict(lambda: 0)
        self.defaults = [
            [[None, 1, 20, 1], [None, 1, 100, 120]],
            [yesterday, yesterday],
            [[None, 1, 10, 60], [None, 1, 10, 60]],
            [yesterday, yesterday]
        ]
        # Rates are recorded as [minumum_call_backed, current_call_passed, max_call_allowed, time_span]

    async def get_limit_token(self, server: str, method: str) -> LimitToken:
        async with self._lock(f'{self._api_key}_{server}_lock'):
            return await super().get_limit_token(server, method)

    async def put_stream(self, fetched: dict, server: str, method: str, token: LimitToken):
        async with self._lock(f'{self._api_key}_{server}_lock'):
            await super().put_stream(fetched, server, method, token)

    async def inmediate_backoff(self, seconds: int, type_: str, server: str, method: str = None):
        async with self._seal:
            await super().inmediate_backoff(seconds, type_, server, method)
    
    async def get_limits(self, server: str, method: str):
        limits = []
        limits.append(f"{self._api_key}_application_rates_{server}")
        limits.append(f"{self._api_key}_application_times_{server}")
        limits.append(f"{self._api_key}_methods_rates_{method}")
        limits.append(f"{self._api_key}_methods_times_{method}")
        responses = enumerate(self._redis.mget(limits))
        # responses = enumerate(await thread_run(partial(self._redis.mget, limits)))
        return [pytify(item) if item is not None else fast_copy(self.defaults[ind]) for (ind, item) in responses]

    async def set_limits(self, server: str, method: str, limits: List[Any]):
        mapping = {}
        r_app_rate = limits[0]
        r_app_time = limits[1]
        r_method_rate = limits[2]
        r_method_time = limits[3]
        mapping[f"{self._api_key}_application_rates_{server}"] = bytify(r_app_rate)
        mapping[f"{self._api_key}_application_times_{server}"] = bytify(r_app_time)
        mapping[f"{self._api_key}_methods_rates_{method}"] = bytify(r_method_rate)
        mapping[f"{self._api_key}_methods_times_{method}"] = bytify(r_method_time)
        pipe = self._redis.pipeline()
        for key, val in mapping.items():
            pipe.set(key, val, 3600)
        pipe.execute()
        # await thread_run(pipe.execute)
