import datetime
from datetime import timedelta as td
from typing import Callable, Any, TypeVar, Dict
from logging import getLogger
import copy
import atexit

from diskcache import FanoutCache
from asgiref.sync import sync_to_async
from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.objects import StoreObject
from pyot.pipeline.expiration import ExpirationManager
from pyot.utils import bytify, pytify

LOGGER = getLogger(__name__)


class DiskCache(StoreObject):
    unique = False
    store_type = "CACHE"

    def __init__(self, game: str, directory: str, expirations: Any = None, log_level: int = 10, **kwargs) -> None:
        self._game = game
        kwargs = {key.lower():val for (key,val) in kwargs.items()}
        if "timeout" not in kwargs: kwargs["timeout"] = 1
        self._cache = FanoutCache(directory=directory, **kwargs)
        self._alias = str(directory).split("/")[-1] if "/" in str(directory) else str(directory).split("\\")[-1]
        self._manager = ExpirationManager(game, expirations)
        self._log_level = log_level
        atexit.register(self._cache.close)

    async def set(self, token: PipelineToken, value: Any) -> None:
        timeout = self._manager.get_timeout(token.method)
        if timeout != 0:
            if timeout == -1:
                timeout = None
            await sync_to_async(self._cache.set)(token.stringify, bytify(value), timeout)
            LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DiskCache > {self._alias}] SET: {self._log_template(token)}")

    async def get(self, token: PipelineToken, session = None) -> Any:
        timeout = self._manager.get_timeout(token.method)
        if timeout == 0:
            raise NotFound
        item = await sync_to_async(self._cache.get)(token.stringify)
        if item is None:
            raise NotFound
        LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DiskCache > {self._alias}] GET: {self._log_template(token)}")
        return pytify(item)

    async def delete(self, token: PipelineToken) -> None:
        await sync_to_async(self._cache.delete)(token.stringify)
        LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DiskCache > {self._alias}] DELETE: {self._log_template(token)}")

    async def contains(self, token: PipelineToken) -> bool:
        item = await sync_to_async(self._cache.get)(token.stringify)
        if item is None:
            return False
        return True

    async def clear(self):
        await sync_to_async(self._cache.clear)()
        LOGGER.log(self._log_level, f"[Trace: {self._game.upper()} > DiskCache > {self._alias}] CLEAR: Store has been cleared successfully")
