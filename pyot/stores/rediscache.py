from typing import Any
import aioredis

from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.expiration import ExpirationManager
from pyot.utils.parsers import to_bytes, from_bytes
from pyot.utils.eventloop import EventLoopFactory
from pyot.utils.logging import Logger

from .base import Store, StoreType


LOGGER = Logger(__name__)


class RedisCache(Store):

    type = StoreType.CACHE

    def __init__(self, game: str, host='127.0.0.1', port=6379, db=0, expirations: Any = None, log_level: int = 0, kwargs=None) -> None:
        self.game = game
        kwargs = kwargs or {}
        self.location = f"{host}:{port}/{db}"
        self.data = EventLoopFactory(
            factory=lambda: aioredis.create_redis_pool(f"redis://{host}:{port}/{db}", **kwargs),
            callback=lambda x: x.close(),
        )
        self.expirations = ExpirationManager(game, expirations)
        self.log_level = log_level

    async def get(self, token: PipelineToken, **kwargs) -> Any:
        timeout = self.expirations.get_timeout(token.method)
        if timeout == 0:
            raise NotFound(token.value)
        cache = await self.data.get()
        item = await cache.get(token.value)
        if item is None:
            raise NotFound(token.value)
        LOGGER.log(self.log_level, f"[Trace: {self.game} > RedisCache > {self.location}] GET: {token.value}")
        return from_bytes(item)

    async def set(self, token: PipelineToken, value: Any, **kwargs) -> None:
        timeout = self.expirations.get_timeout(token.method)
        if timeout != 0:
            if timeout == -1:
                timeout = None
            cache = await self.data.get()
            await cache.set(token.value, to_bytes(value), expire=timeout)
            LOGGER.log(self.log_level, f"[Trace: {self.game} > RedisCache > {self.location}] SET: {token.value}")

    async def delete(self, token: PipelineToken, **kwargs) -> None:
        cache = await self.data.get()
        await cache.delete(token.value)
        LOGGER.log(self.log_level, f"[Trace: {self.game} > RedisCache > {self.location}] DELETE: {token.value}")

    async def contains(self, token: PipelineToken, **kwargs) -> bool:
        cache = await self.data.get()
        item = await cache.get(token.value)
        if item is None:
            return False
        return True

    async def clear(self, **kwargs):
        cache = await self.data.get()
        await cache.flushall()
        LOGGER.log(self.log_level, f"[Trace: {self.game} > RedisCache > {self.location}] CLEAR: Store has been cleared successfully")
