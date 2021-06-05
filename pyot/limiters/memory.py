from time import time
from typing import Dict, List, Union

from aiohttp import ClientResponse

from pyot.utils.locks import SealLock

from .base import BaseLimiter, LimiterToken


class MemoryLimiterDict(dict):

    def get(self, k: str) -> int:
        try:
            return self.__getitem__(k)
        except KeyError:
            return None

    def set(self, k: str, v: int, nx=False):
        if nx and k not in self or not nx:
            self.__setitem__(k, v)
            return 1
        return 0

    def incr(self, k):
        self.__setitem__(k, super().get(k, 0) + 1)

    def decr(self, k):
        self.__setitem__(k, super().get(k, 0) - 1)


class MemoryLimiter(BaseLimiter):

    def __init__(self, game: str, api_key: str, limiting_share: int = 1):
        self.game = game
        self.api_key = api_key
        self.api_hash = api_key[-5:]
        self.limiting_share = limiting_share
        self.lock = SealLock()
        self.entries = MemoryLimiterDict()

    async def get_token(self, server: str, method: str):
        sleep = 0
        allowed = []
        pinging_list = []
        epoch = 0
        async with self.lock:
            app_prefix = f'{self.api_hash}:{self.game}:{server}'
            method_prefix = f'{self.api_hash}:{self.game}:{server}:{method}'
            now = epoch = time()
            for prefix, i, type in ((app_prefix, 0, "app"), (app_prefix, 1, "app"), (method_prefix, 0, "method"), (method_prefix, 1, "method")):
                prefix_i = f'{prefix}:{i}'
                exists = self.entries.get(f'{prefix_i}:exists')
                if exists == 0:
                    continue
                freeze = self.entries.get(f'{prefix_i}:freeze')
                if (freeze or 0) > now:
                    sleep = max(sleep, freeze - now)
                    continue
                pinging = self.entries.get(f'{prefix_i}:pinging')
                pingexp = self.entries.get(f'{prefix_i}:pingexp')
                if now > (pingexp or 0):
                    pinging = 0
                if pinging:
                    sleep = max(sleep, 0.1)
                    break
                maxcall = self.entries.get(f'{prefix_i}:maxcall')
                rollover = self.entries.get(f'{prefix_i}:rollover')
                timespan = self.entries.get(f'{prefix_i}:timespan')
                called = self.entries.get(f'{prefix_i}:called')
                begintime = self.entries.get(f'{prefix_i}:begintime')
                pingtime = self.entries.get(f'{prefix_i}:pingtime')
                if maxcall is not None:
                    blackout = begintime + timespan
                    nextstart = blackout + pingtime
                    qualified = nextstart - now
                if maxcall is None or now > nextstart:
                    self.entries.set(f'{prefix_i}:pinging', 1)
                    self.entries.set(f'{prefix_i}:pingexp', now + 10)
                    self.entries.set(f'{prefix_i}:pingbegintime', now)
                    pinging_list.append((prefix_i, type, i))
                    continue
                # print(called, maxcall, now, nextstart, qualified)
                if (rollover or 0) + called >= maxcall:
                    sleep = max(sleep, qualified)
                    continue
                if now >= blackout:
                    sleep = max(sleep, qualified)
                    continue
                # print(pingtime)
                allowed.append(prefix_i)
            if sleep == 0:
                for allow in allowed:
                    self.entries.incr(f'{allow}:called')
                    if len(pinging_list) == 0:
                        self.entries.incr(f'{allow}:flying')
            else:
                for (prefix_i, type, _) in pinging_list:
                    self.entries.set(f'{prefix_i}:pinging', 0)
        return LimiterToken(server, method, epoch, sleep, allowed, pinging_list)

    async def sync_rates(self, token: LimiterToken, response: ClientResponse) -> Dict[str, List[List[int]]]:
        header = self.parse_headers(response)
        if header is None:
            await self.ping_fail(token)
            return
        if token.pinging:
            async with self.lock:
                now = time()
                for (prefix_i, type, i) in token.pinging:
                    if i >= len(header[f'{type}_limit']):
                        self.entries.set(f'{prefix_i}:exists', 0)
                    else:
                        # print(prefix_i, header[f'{type}_limit'][i][0], header[f'{type}_limit'][i][1], header[f'{type}_count'][i][0])
                        self.entries.set(f'{prefix_i}:exists', 1)
                        self.entries.set(f'{prefix_i}:maxcall', header[f'{type}_limit'][i][0])
                        self.entries.set(f'{prefix_i}:timespan', header[f'{type}_limit'][i][1])
                        self.entries.set(f'{prefix_i}:called', header[f'{type}_count'][i][0])
                        self.entries.set(f'{prefix_i}:rollover', self.entries.get(f'{prefix_i}:flying'))
                        self.entries.set(f'{prefix_i}:flying', 0)
                        begintime = self.entries.get(f'{prefix_i}:pingbegintime')
                        self.entries.set(f'{prefix_i}:begintime', begintime)
                        self.entries.set(f'{prefix_i}:pingtime', now - begintime)
                        self.entries.set(f'{prefix_i}:pinging', 0)
        else:
            async with self.lock:
                for prefix_i in token.allowed:
                    begintime = self.entries.get(f'{prefix_i}:begintime')
                    if token.epoch >= begintime:
                        self.entries.decr(f'{prefix_i}:flying')
        return header

    async def ping_fail(self, token: LimiterToken):
        async with self.lock:
            for (prefix_i, _, _) in token.pinging:
                self.entries.set(f'{prefix_i}:pinging', 0)

    async def freeze_rates(self, token: LimiterToken, response: ClientResponse) -> Dict[str, Union[str, int]]:
        header = self.parse_429(response)
        now = time()
        async with self.lock:
            for (prefix_i, type, _) in token.pinging:
                if type != header["type"]:
                    continue
                self.entries.set(f'{prefix_i}:freeze', now + header["time"])
        return header
