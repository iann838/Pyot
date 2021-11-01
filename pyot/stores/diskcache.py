from typing import Any
import atexit

from diskcache import FanoutCache
from asgiref.sync import sync_to_async
from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.expiration import ExpirationManager
from pyot.utils.parsers import to_bytes, from_bytes
from pyot.utils.logging import Logger

from .base import Store, StoreType


LOGGER = Logger(__name__)


class DiskCache(Store):

    type = StoreType.CACHE

    def __init__(self, game: str, directory: str, expirations: Any = None, log_level: int = 0, kwargs=None) -> None:
        self.game = game
        kwargs = kwargs or {}
        if "timeout" not in kwargs: kwargs["timeout"] = 1
        self._cache = FanoutCache(directory=directory, **kwargs)
        self._alias = str(directory).split("/")[-1] if "/" in str(directory) else str(directory).split("\\")[-1]
        self._manager = ExpirationManager(game, expirations)
        self.log_level = log_level
        atexit.register(self._cache.close)

    async def set(self, token: PipelineToken, value: Any, **kwargs) -> None:
        timeout = self._manager.get_timeout(token.method)
        if timeout != 0:
            if timeout == -1:
                timeout = None
            await sync_to_async(self._cache.set)(token.value, to_bytes(value), timeout)
            LOGGER.log(self.log_level, f"[Trace: {self.game} > DiskCache > {self._alias}] SET: {token.value}")

    async def get(self, token: PipelineToken, **kwargs) -> Any:
        timeout = self._manager.get_timeout(token.method)
        if timeout == 0:
            raise NotFound(token.value)
        item = await sync_to_async(self._cache.get)(token.value)
        if item is None:
            raise NotFound(token.value)
        LOGGER.log(self.log_level, f"[Trace: {self.game} > DiskCache > {self._alias}] GET: {token.value}")
        return from_bytes(item)

    async def delete(self, token: PipelineToken, **kwargs) -> None:
        await sync_to_async(self._cache.delete)(token.value)
        LOGGER.log(self.log_level, f"[Trace: {self.game} > DiskCache > {self._alias}] DELETE: {token.value}")

    async def contains(self, token: PipelineToken, **kwargs) -> bool:
        item = await sync_to_async(self._cache.get)(token.value)
        if item is None:
            return False
        return True

    async def clear(self, **kwargs):
        await sync_to_async(self._cache.clear)()
        LOGGER.log(self.log_level, f"[Trace: {self.game} > DiskCache > {self._alias}] CLEAR: Store has been cleared successfully")
