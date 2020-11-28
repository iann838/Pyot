from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
from functools import partial
from logging import getLogger
from typing import List, Any
from dateutil.parser import parse
import asyncio
import pickle
import pytz

from pyot.utils import SealLock, MultiDefaultDict

LOGGER = getLogger(__name__)


@dataclass
class LimitToken:
    _token: List[int] = field(default_factory=list)
    flag_app: bool = False
    flag_method: bool = False

    def append(self, val: int):
        self._token.append(val)

    @property
    def max(self) -> int:
        val = max(self._token)
        if val >= 0:
            return val
        else:
            return 0

    async def run_or_wait(self):
        max_ = self.max
        if max_ > 0:
            await asyncio.sleep(max_)
            return True
        else:
            return False


class BaseLimiter:
    last_waited: datetime
    
    def __init__(self, game, api_key, limiting_share=1):
        yesterday = datetime.now(pytz.utc) - timedelta(days=1)
        self._game = game
        self._limiting_share = limiting_share
        self._api_key = api_key
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
        token = LimitToken()
        r_app_rate, r_app_time, r_method_rate, r_method_time = await self.get_limits(server, method)
        app_rate1 = r_app_rate[0]
        app_rate2 = r_app_rate[1]
        app_time1 = r_app_time[0]
        app_time2 = r_app_time[1]
        now = datetime.now(pytz.utc)
        method_rate1 = r_method_rate[0]
        method_rate2 = r_method_rate[1]
        method_time1 = r_method_time[0]
        method_time2 = r_method_time[1]
        if app_time1 < now:
            # app_time1 = r_app_time[0] = now + timedelta(seconds=app_rate1[3])
            app_rate1[0] = r_app_rate[0][0] = None
            app_rate1[1] = r_app_rate[0][1] = 0
        if app_time2 < now:
            # app_time2 = r_app_time[1] = now + timedelta(seconds=app_rate2[3])
            app_rate2[0] = r_app_rate[1][0] = None
            app_rate2[1] = r_app_rate[1][1] = 0
        if method_time1 < now:
            # method_time1 = r_method_time[0] = now + timedelta(seconds=method_rate1[3])
            method_rate1[0] = r_method_rate[0][0] = None
            method_rate1[1] = r_method_rate[0][1] = 0
        if method_time2 < now:
            # method_time2 = r_method_time[1] = now + timedelta(seconds=method_rate2[3])
            method_rate2[0] = r_method_rate[1][0] = None
            method_rate2[1] = r_method_rate[1][1] = 0

        i_rates = [app_rate1, app_rate2, method_rate1, method_rate2]
        i_times = [app_time1, app_time2, method_time1, method_time2]
        
        for i in range(4):
            if i_rates[i][0] and i_rates[i][0] + i_rates[i][1] >= int(i_rates[i][2]*self._limiting_share):
                token.append((i_times[i]-now).total_seconds())
            else:
                token.append(0)

        if self._application_backoffs[server] > now:
            token.append((self._application_backoffs[server]-now).total_seconds())

        if self._methods_backoffs[method] > now:
            token.append((self._methods_backoffs[method]-now).total_seconds())


        if token.max == 0:
            try:
                _ = self.last_waited
            except AttributeError:
                self.last_waited = now

            if r_app_rate[0][0] is None and self._application_bucket[server] == 0:
                self._application_bucket[server] += 1
                self.last_waited = now + timedelta(seconds=3)
                token.flag_app = True
                token.append(0)
            elif r_app_rate[0][0] is None and self._application_bucket[server] > 0:
                if self.last_waited < now:
                    self._application_bucket[server] = 0
                token.append(0.03)

            if r_method_rate[0][0] is None and self._methods_bucket[method] == 0:
                self._methods_bucket[method] += 1
                self.last_waited = now + timedelta(seconds=3)
                token.flag_method = True
                token.append(0)
            elif r_method_rate[0][0] is None and self._methods_bucket[method] > 0:
                if self.last_waited < now:
                    self._methods_bucket[method] = 0
                token.append(0.03)

        if token.max == 0:
            for i in range(4):
                i_rates[i][1] += 1

        await self.set_limits(server, method, [r_app_rate, r_app_time, r_method_rate, r_method_time])
        return token

    async def stream(self, response: Any, server: str, method: str, token: LimitToken):
        headers = response.headers if hasattr(response, "headers") else None
        if headers is None:
            self.validate_bucket(server, method, token)
        try:
            date = parse(headers["Date"].split(', ')[1])
            app_limit = [[int(val) for val in token.split(':')] for token in headers["X-App-Rate-Limit"].split(',')]
            app_count = [[int(val) for val in token.split(':')] for token in headers["X-App-Rate-Limit-Count"].split(',')]
            method_limit = [[int(val) for val in token.split(':')] for token in headers["X-Method-Rate-Limit"].split(',')]
            method_count = [[int(val) for val in token.split(':')] for token in headers["X-Method-Rate-Limit-Count"].split(',')]
            if len(method_limit) == 1:
                method_limit.append(method_limit[0])
            if len(method_count) == 1:
                method_count.append(method_count[0])
            fetched = {
                "date": date,
                "app_limit": app_limit,
                "app_count": app_count,
                "method_limit": method_limit,
                "method_count": method_count,
            }
            await self.put_stream(fetched, server, method, token)
        except KeyError:
            self.validate_bucket(server, method, token)
        except Exception as e:
            LOGGER.warning(f"[Trace: {self._game.upper()} > RiotAPI] WARNING: Exception '{str(e)}' happened while streaming to rate limiter")

    async def put_stream(self, fetched: dict, server: str, method: str, token: LimitToken):
        now = datetime.now(pytz.utc)
        date = fetched["date"]
        app_limit = fetched["app_limit"]
        app_count = fetched["app_count"]
        method_limit = fetched["method_limit"]
        method_count = fetched["method_count"]
        r_app_rate, r_app_time, r_method_rate, r_method_time = await self.get_limits(server, method)
        for i in range(2):
            if r_app_rate[0][i+2] != app_limit[0][i]:
                r_app_rate[0][i+2] = app_limit[0][i]
            if r_app_rate[1][i+2] != app_limit[1][i]:
                r_app_rate[1][i+2] = app_limit[1][i]
            if r_method_rate[0][i+2] != method_limit[0][i]:
                r_method_rate[0][i+2] = method_limit[0][i]
            if r_method_rate[1][i+2] != method_limit[1][i]:
                r_method_rate[1][i+2] = method_limit[1][i]
        for i in range(2):
            if token.flag_app and self._application_bucket[server] > 0:
                self._application_bucket[server] -= 1
            if token.flag_method and self._methods_bucket[method] > 0:
                self._methods_bucket[method] -= 1
        for i in range(2):
            if not r_app_rate[i][0] or app_count[i][0] < r_app_rate[i][0]:
                r_app_rate[i][0] = app_count[i][0]
            if not r_method_rate[i][0] or method_count[i][0] < r_method_rate[i][0]:
                r_method_rate[i][0] = method_count[i][0]
        for i in range(2):
            if token.flag_app and r_app_time[i] < now:
                app_top = date + timedelta(seconds=r_app_rate[i][3] - 0.03)
                r_app_time[i] = app_top
            if token.flag_method and r_method_time[i] < now:
                method_top = date + timedelta(seconds=r_method_rate[i][3] - 0.03)
                r_method_time[i] = method_top
        await self.set_limits(server, method, [r_app_rate, r_app_time, r_method_rate, r_method_time])

    async def inmediate_backoff(self, seconds: int, type_: str, server: str, method: str = None):
        time = datetime.now(pytz.utc) + timedelta(seconds=seconds)
        if type_ == "application":
            self._application_backoffs[server] = time
        else:
            self._methods_backoffs[method] = time

    async def get_limits(self, server: str, method: str):
        limits = []
        limits.append(self._application_rates[server])
        limits.append(self._application_times[server])
        limits.append(self._methods_rates[method])
        limits.append(self._methods_times[method])
        return limits

    async def set_limits(self, server: str, method: str, limits: List[Any]):
        r_app_rate = limits[0]
        r_app_time = limits[1]
        r_method_rate = limits[2]
        r_method_time = limits[3]
        self._application_rates[server] = r_app_rate
        self._application_times[server] = r_app_time
        self._methods_rates[method] = r_method_rate
        self._methods_times[method] = r_method_time

    def validate_bucket(self, server, method, token: LimitToken):
        if token.flag_app:
            self._application_bucket[server] -= 1
        if token.flag_method:
            self._methods_bucket[method] -= 1
