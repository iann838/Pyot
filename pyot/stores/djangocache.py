from typing import Any

from django.core.cache import caches
from asgiref.sync import sync_to_async
from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.expiration import ExpirationManager
from pyot.utils.logging import Logger

from .base import Store, StoreType


LOGGER = Logger(__name__)


class DjangoCache(Store):

    type = StoreType.CACHE

    def __init__(self, game: str, alias: str = None, expirations: Any = None, log_level: int = 0) -> None:
        if alias is None: raise ValueError("Argument 'ALIAS' is obligatory for Store 'DjangoCache' to be able to point the correct cache")
        self.game = game
        self.alias = alias
        self.data = caches[alias]
        self.expirations = ExpirationManager(game, expirations)
        self.log_level = log_level

    async def set(self, token: PipelineToken, value: Any, **kwargs) -> None:
        timeout = self.expirations.get_timeout(token.method)
        if timeout != 0:
            if timeout == -1:
                timeout = None
            await sync_to_async(self.data.set)(token.value, value, timeout)
            LOGGER.log(self.log_level, f"[Trace: {self.game} > DjangoCache > {self.alias}] SET: {token.value}")

    async def get(self, token: PipelineToken, **kwargs) -> Any:
        timeout = self.expirations.get_timeout(token.method)
        if timeout == 0:
            raise NotFound(token.value)
        item = await sync_to_async(self.data.get)(token.value)
        if item is None:
            raise NotFound(token.value)
        LOGGER.log(self.log_level, f"[Trace: {self.game} > DjangoCache > {self.alias}] GET: {token.value}")
        return item

    async def delete(self, token: PipelineToken, **kwargs) -> None:
        await sync_to_async(self.data.delete)(token.value)
        LOGGER.log(self.log_level, f"[Trace: {self.game} > DjangoCache > {self.alias}] DELETE: {token.value}")

    async def contains(self, token: PipelineToken, **kwargs) -> bool:
        item = await sync_to_async(self.data.get)(token.value)
        if item is None:
            return False
        return True

    async def clear(self, **kwargs):
        await sync_to_async(self.data.clear)()
        LOGGER.log(self.log_level, f"[Trace: {self.game} > DjangoCache > {self.alias}] CLEAR: Store has been cleared successfully")
