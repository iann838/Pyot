import datetime
from typing import Callable, Any, TypeVar, Dict
from logging import getLogger

from django.core.cache import caches
from asgiref.sync import sync_to_async
from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.objects import StoreObject
from pyot.pipeline.expiration import ExpirationManager

LOGGER = getLogger(__name__)


class DjangoCache(StoreObject):
    unique = False
    store_type = "CACHE"

    def __init__(self, game: str, alias: str = None, expirations: Any = None, log_level: int = 10) -> None:
        if alias is None: raise RuntimeError("Argument 'ALIAS' is obligatory for Store 'DjangoCache' because Pyot will not guess which cache is used")
        self._game = game
        self._alias = alias
        self._cache = caches[alias]
        self._manager = ExpirationManager(game, expirations)
        self._log_level = log_level

    async def set(self, token: PipelineToken, value: Any) -> None:
        timeout = self._manager.get_timeout(token.method)
        if timeout != 0:
            if timeout == -1:
                timeout = None
            await sync_to_async(self._cache.set)(token.stringify, value, timeout)
            LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DjangoCache > {self._alias}] SET: {self._log_template(token)}")

    async def get(self, token: PipelineToken, session = None) -> Any:
        timeout = self._manager.get_timeout(token.method)
        if timeout == 0:
            raise NotFound
        item = await sync_to_async(self._cache.get)(token.stringify)
        if item is None:
            raise NotFound
        LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DjangoCache > {self._alias}] GET: {self._log_template(token)}")
        return item

    async def delete(self, token: PipelineToken) -> None:
        await sync_to_async(self._cache.delete)(token.stringify)
        LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DjangoCache > {self._alias}] DELETE: {self._log_template(token)}")

    async def contains(self, token: PipelineToken) -> bool:
        item = await sync_to_async(self._cache.get)(token.stringify)
        if item is None:
            return False
        return True
    
    # This function is really not needed.
    # It is more than a helper func if you're not familiar with django cache.
    # Django way of clearing:
    # terminal/cmd: `python manage.py shell`
    # >>> from django.core.cache import caches
    # >>> caches[name_of_your_cache].clear()
    async def clear(self):
        await sync_to_async(self._cache.clear)()
        LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DjangoCache > {self._alias}] CLEAR: Store has been cleared successfully")
