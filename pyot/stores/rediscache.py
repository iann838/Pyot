from typing import Any
import aioredis
import pickle

from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.expiration import ExpirationManager
from pyot.core.resources import ResourceTemplate
from pyot.utils.logging import LazyLogger

from .base import Store, StoreType


LOGGER = LazyLogger(__name__)


class RedisCache(Store):

    type = StoreType.CACHE

    def __init__(self, game: str, host='127.0.0.1', port=6379, db=0, expirations: Any = None, log_level: int = 0, **kwargs) -> None:
        self.game = game
        self.location = f"{host}:{port}/{db}"
        self.redises = ResourceTemplate(
            acquire_func=lambda: aioredis.Redis(host=host, port=port, db=db, **kwargs),
            release_func=lambda x: x.close(),
        )
        self.expirations = ExpirationManager(game, expirations)
        self.log_level = log_level

    async def get(self, token: PipelineToken, **kwargs) -> Any:
        timeout = self.expirations.get_timeout(token.method)
        if timeout == 0:
            raise NotFound(token.value)
        cache = await self.redises.acquire()
        item = await cache.get(token.value)
        if item is None:
            raise NotFound(token.value)
        LOGGER.log(self.log_level, f"[pyot.stores.rediscache:RedisCache#{self.location}] GET {token.value}")
        return pickle.loads(item)

    async def set(self, token: PipelineToken, value: Any, **kwargs) -> None:
        timeout = self.expirations.get_timeout(token.method)
        if timeout != 0:
            if timeout == -1:
                timeout = None
            cache = await self.redises.acquire()
            await cache.set(token.value, pickle.dumps(value), ex=timeout)
            LOGGER.log(self.log_level, f"[pyot.stores.rediscache:RedisCache#{self.location}] SET {token.value}")

    async def delete(self, token: PipelineToken, **kwargs) -> None:
        cache = await self.redises.acquire()
        await cache.delete(token.value)
        LOGGER.log(self.log_level, f"[pyot.stores.rediscache:RedisCache#{self.location}] DELETE {token.value}")

    async def contains(self, token: PipelineToken, **kwargs) -> bool:
        cache = await self.redises.acquire()
        item = await cache.get(token.value)
        if item is None:
            return False
        return True

    async def clear(self, **kwargs):
        cache = await self.redises.acquire()
        await cache.flushdb()
        LOGGER.log(self.log_level, f"[pyot.stores.rediscache:RedisCache#{self.location}] Store cleared successfully")
