from abc import ABC, abstractproperty
from enum import Enum


class StoreType(Enum):
    SERVICE = "service"
    CACHE = "cache"


class Store(ABC):

    @property
    def classname(self):
        return self.__class__.__name__

    @abstractproperty
    def type(self) -> StoreType:
        raise NotImplementedError

    # Service store methods:

    async def request(self, method, token, *args, **kwargs):
        raise NotImplementedError

    async def get(self, token, *args, **kwargs):
        return await self.request("GET", token, *args, **kwargs)

    async def post(self, token, body, *args, **kwargs):
        return await self.request("POST", token, body, *args, **kwargs)

    async def put(self, token, body, *args, **kwargs):
        return await self.request("PUT", token, body, *args, **kwargs)

    # Cache store methods:

    async def set(self, token, response, *args, **kwargs):
        raise NotImplementedError

    async def clear(self, *args, **kwargs):
        raise NotImplementedError

    async def expire(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, token, *args, **kwargs):
        raise NotImplementedError

    async def contains(self, token, *args, **kwargs):
        raise NotImplementedError
