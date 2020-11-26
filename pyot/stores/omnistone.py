import datetime
from typing import Callable, Any, TypeVar, Tuple, Dict
from datetime import timedelta as td
from logging import getLogger
import pickle
import copy

from pyot.utils import SealLock
from pyot.core.exceptions import NotFound
from pyot.pipeline.objects import StoreObject
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.expiration import ExpirationManager

LOGGER = getLogger(__name__)


class Omnistone(StoreObject):
    unique = True
    store_type = "CACHE"

    def __init__(self, game: str, expirations: Any = None, max_entries: int = 10000, cull_frecuency: int = 2, log_level: int = 10) -> None:
        self._game = game
        self._data = dict()
        self._lock = SealLock()
        self._manager = ExpirationManager(game, expirations)
        self._max_entries = max_entries
        self._cull_frecuency = cull_frecuency
        self._cull_lock = [False, datetime.datetime.now()]
        self._log_level = log_level

    async def set(self, token: PipelineToken, value: Any) -> None:
        timeout = self._manager.get_timeout(token.method)
        if timeout != 0:
            async with self._lock:
                if timeout != -1:
                    timeout = datetime.timedelta(seconds=timeout)
                if await self._allowed():
                    value = pickle.dumps(value)
                    self._data[token] = (value, timeout, datetime.datetime.now(), datetime.datetime.now())
                    LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > Omnistone] SET: {self._log_template(token)}")
            if len(self._data) > self._max_entries and await self._allowed():
                async with self._lock:
                    self._cull_lock = [True, datetime.datetime.now()]
                await self.expire()
                if len(self._data) > self._max_entries - self._max_entries/self._cull_frecuency:
                    await self.cull()

    async def get(self, token: PipelineToken, expiring: bool = False, session = None) -> Any:
        timeout = self._manager.get_timeout(token.method)
        if timeout == 0:
            raise NotFound
        async with self._lock:
            try:
                item, timeout, entered, _ = self._data[token]
            except KeyError:
                raise NotFound
            if not expiring:
                LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > Omnistone] GET: {self._log_template(token)}")

            now = datetime.datetime.now()
            if timeout == -1:
                self._data[token] = (item, timeout, entered, now)
                item = pickle.loads(item)
                return item
            
            elif now > entered + timeout:
                try:
                    del self._data[token]
                except: pass
                raise NotFound
            
            else:
                self._data[token] = (item, timeout, entered, now)
                item = pickle.loads(item)
                return item

    async def delete(self, token: PipelineToken) -> None:
        try:
            del self._data[token]
            LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > Omnistone] DELETE: {self._log_template(token)}")
        except KeyError:
            raise NotFound

    async def expire(self):
        for token in self._data:
            await self.get(token, expiring=True)

    async def clear(self):
        async with self._lock:
            self._data = {}
            LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > Omnistone] CLEAR: Store has been cleared successfully")

    async def _allowed(self):
        if not self._cull_lock[0]:
            return True
        elif self._cull_lock[0] and datetime.datetime.now() > self._cull_lock[1] + datetime.timedelta(seconds=30):
            self._cull_lock[0] = False
            return True
        else:
            return False

    async def cull(self):
        async with self._lock:
            data = copy.copy(self._data)
        lru = sorted(data.keys(), key=lambda x: data[x][3])
        for token in lru[:int(len(data)/self._cull_frecuency)]:
            await self.delete(token)
        self._cull_lock[0] = False

    async def contains(self, token: PipelineToken) -> bool:
        try:
            _ = self._data[token]
            return True
        except KeyError:
            return False
