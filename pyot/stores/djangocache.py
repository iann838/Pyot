from typing import Callable, Any, TypeVar
from django.core.cache import caches
from .__core__ import PyotStoreObject, PyotExpirationManager
from ..core.pipeline import PyotPipelineToken
from ..core.exceptions import NotFound
import datetime

from logging import getLogger
LOGGER = getLogger(__name__)


class DjangoCache(PyotStoreObject):
    unique = False

    def __init__(self, game: str, alias: str = None, expirations: Any = None, logs_enabled: bool = True) -> None:
        if alias is None: raise RuntimeError("Argument 'ALIAS' is obligatory for Store 'DjangoCache' because Pyot will not guess which cache is used")
        self._game = game
        self._alias = alias
        self._cache = caches[alias]
        self._manager = PyotExpirationManager(game, expirations)
        self._logs_enabled = logs_enabled

    async def put(self, token: PyotPipelineToken, value: Any) -> None:
        timeout = self._manager.get_timeout(token.method)
        if timeout != 0:
            if timeout == -1:
                timeout = None
            self._cache.set(token.stringify, value, timeout)
            if self._logs_enabled:
                LOGGER.warn(f"[Trace: {self._game.upper()} > DjangoCache > {self._alias}] PUT: {self._log_template(token)}")

    async def get(self, token: PyotPipelineToken, session = None) -> Any:
        timeout = self._manager.get_timeout(token.method)
        if timeout == 0:
            raise NotFound
        item = self._cache.get(token.stringify)
        if item is None:
            raise NotFound
        if self._logs_enabled:
            LOGGER.warn(f"[Trace: {self._game.upper()} > DjangoCache > {self._alias}] GET: {self._log_template(token)}")
        return item

    def delete(self, token: PyotPipelineToken) -> None:
        self._cache.delete(token.stringify)
        if self._logs_enabled:
            LOGGER.warn(f"[Trace: {self._game.upper()} > DjangoCache > {self._alias}] DELETE: {self._log_template(token)}")

    def contains(self, token: PyotPipelineToken) -> bool:
        item = self._cache.get(token.stringify)
        if item is None:
            return False
        return True
    
    # This function is really not needed.
    # It is more than a helper func if you're not familiar with django cache.
    # Django way of clearing:
    # terminal/cmd: `python manage.py shell`
    # >>> from django.core.cache import caches
    # >>> caches[name_of_your_cache].clear()
    def clear(self):
        self._cache.clear()
        if self._logs_enabled:
            LOGGER.warn(f"[Trace: {self._game.upper()} > DjangoCache > {self._alias}] CLEAR: Store has been cleared successfully")

