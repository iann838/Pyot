from typing import Callable, Any, TypeVar, Tuple
from threading import Lock
from .__core__ import PyotStoreObject, PyotExpirationManager
from ..core.pipeline import PyotPipelineToken
from ..core.exceptions import NotFound
from ..core.lock import PyotLock
import datetime
import copy

from logging import getLogger
LOGGER = getLogger(__name__)


class Omnistone(PyotStoreObject):
    unique = True

    def __init__(self, game: str, expirations: Any = None, max_entries: int = 10000, cull_frecuency: int = 2, logs_enabled: bool = True) -> None:
        self._game = game
        self._data = dict()
        self._lock = PyotLock()
        self._manager = PyotExpirationManager(game, expirations)
        self._max_entries = max_entries
        self._cull_frecuency = cull_frecuency
        self._cull_lock = [False, datetime.datetime.now()]
        self._logs_enabled = logs_enabled

    async def put(self, token: PyotPipelineToken, value: Any) -> None:
        timeout = self._manager.get_timeout(token.method)
        if timeout != 0:
            async with self._lock:
                if timeout != -1:
                    timeout = datetime.timedelta(seconds=timeout)
                if await self._allowed():
                    self._data[token] = (value, timeout, datetime.datetime.now(), datetime.datetime.now())
                    if self._logs_enabled:
                        LOGGER.warning(f"[Trace: {self._game.upper()} > Omnistone] PUT: {self._log_template(token)}")
            if len(self._data) > self._max_entries and await self._allowed():
                async with self._lock:
                    if self._logs_enabled:
                        LOGGER.warning(f"[Trace: {self._game.upper()} > Omnistone] VACUUM: Expiration check starts")
                    self._cull_lock = [True, datetime.datetime.now()]
                await self.expire()
                if len(self._data) > self._max_entries - self._max_entries/self._cull_frecuency:
                    await self.cull()

    async def get(self, token: PyotPipelineToken, expiring: bool = False, session = None) -> Any:
        timeout = self._manager.get_timeout(token.method)
        if timeout == 0:
            raise NotFound
        async with self._lock:
            try:
                item, timeout, entered, _ = self._data[token]
            except KeyError:
                raise NotFound
            if self._logs_enabled and not expiring:
                LOGGER.warning(f"[Trace: {self._game.upper()} > Omnistone] GET: {self._log_template(token)}")

            now = datetime.datetime.now()
            if timeout == -1:
                self._data[token] = (item, timeout, entered, now)
                return item
            
            elif now > entered + timeout:
                try:
                    del self._data[token]
                    if self._logs_enabled:
                        LOGGER.warning(f"[Trace: {self._game.upper()} > Omnistone] EXPIRE: {self._log_template(token)}")
                except: pass
                raise NotFound
            
            else:
                self._data[token] = (item, timeout, entered, now)
                return item

    async def delete(self, token: PyotPipelineToken) -> None:
        try:
            del self._data[token]
            if self._logs_enabled:
                LOGGER.warning(f"[Trace: {self._game.upper()} > Omnistone] DELETE: {self._log_template(token)}")
        except KeyError:
            raise NotFound

    async def expire(self):
        for token in self._data:
            await self.get(token, expiring=True)

    async def clear(self):
        async with self._lock:
            self._data = {}
            if self._logs_enabled:
                LOGGER.warning(f"[Trace: {self._game.upper()} > Omnistone] CLEAR: Store has been cleared successfully")

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

    async def contains(self, token: PyotPipelineToken) -> bool:
        try:
            _ = self._data[token]
            return True
        except KeyError:
            return False


