from typing import Any
import atexit
import pickle

from diskcache import FanoutCache
from asgiref.sync import sync_to_async
from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.expiration import ExpirationManager
from pyot.utils.logging import LazyLogger

from .base import Store, StoreType


LOGGER = LazyLogger(__name__)


class DiskCache(Store):

    type = StoreType.CACHE

    def __init__(self, game: str, directory: str, expirations: Any = None, log_level: int = 0, **kwargs) -> None:
        self.game = game
        if "timeout" not in kwargs:
            kwargs["timeout"] = 1
        self.cache = FanoutCache(directory=directory, **kwargs)
        self.alias = str(directory).split("/")[-1] if "/" in str(directory) else str(directory).split("\\")[-1]
        self.expirations = ExpirationManager(game, expirations)
        self.log_level = log_level
        atexit.register(self.cache.close)

    async def set(self, token: PipelineToken, value: Any, **kwargs) -> None:
        timeout = self.expirations.get_timeout(token.method)
        if timeout != 0:
            if timeout == -1:
                timeout = None
            await sync_to_async(self.cache.set)(token.value, pickle.dumps(value), timeout)
            LOGGER.log(self.log_level, f"[pyot.stores.diskcache:DiskCache#{self.alias}] SET {token.value}")

    async def get(self, token: PipelineToken, **kwargs) -> Any:
        timeout = self.expirations.get_timeout(token.method)
        if timeout == 0:
            raise NotFound(token.value)
        item = await sync_to_async(self.cache.get)(token.value)
        if item is None:
            raise NotFound(token.value)
        LOGGER.log(self.log_level, f"[pyot.stores.diskcache:DiskCache#{self.alias}] GET {token.value}")
        return pickle.loads(item)

    async def delete(self, token: PipelineToken, **kwargs) -> None:
        await sync_to_async(self.cache.delete)(token.value)
        LOGGER.log(self.log_level, f"[pyot.stores.diskcache:DiskCache#{self.alias}] DELETE {token.value}")

    async def contains(self, token: PipelineToken, **kwargs) -> bool:
        item = await sync_to_async(self.cache.get)(token.value)
        if item is None:
            return False
        return True

    async def clear(self, **kwargs):
        await sync_to_async(self.cache.clear)()
        LOGGER.log(self.log_level, f"[pyot.stores.diskcache:DiskCache#{self.alias}] Store cleared successfully")
