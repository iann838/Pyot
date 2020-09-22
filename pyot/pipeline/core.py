from typing import List, Any, Dict, Callable
from aiohttp import ClientSession
import pickle
import asyncio
import aiohttp

from pyot.core.exceptions import NotFound, NotFindable
from .token import PipelineToken


class Pipeline:
    def __init__(self, model: str, stores: List[Any]):
        self.model = model
        self.stores = stores
        self.sessions = {}

    async def get(self, token: PipelineToken, sid: str = None):
        '''Get an object from the stores.'''
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) if sid is None else self.sessions[sid]
        found_in = None
        try:
            for store in self.stores:
                try:
                    response = await store.get(token, session=session)
                    found_in = store
                except (NotImplementedError, NotFound, NotFindable) as e:
                    if self.stores[-1] == store or store.store_type == "SERVICE" and not isinstance(e, NotFindable):
                        raise
                    continue
                break
        except:
            if sid is None: await session.close()
            raise
        finally:
            if sid is None: await session.close()

        await self.set(token, response, found_in)

        return response

    async def set(self, token: PipelineToken, value: Any, stop=None):
        '''Set an object to stores of type Cache.'''
        for store in self.stores:
            if store is stop: break
            try:
                await store.set(token, value)
            except NotImplementedError:
                continue

    async def post(self, token: PipelineToken, value: Any):
        '''Post an object to stores of type Service.'''
        for store in self.stores:
            try:
                await store.post(token, value)
            except NotImplementedError:
                continue

    async def clear(self):
        '''Clear stores of type Cache.'''
        for store in self.stores:
            try:
                await store.clear()
            except NotImplementedError:
                continue

    async def expire(self):
        '''Expire stores of type Cache that cannot dynamically expire.'''
        for store in self.stores:
            try:
                await store.expire()
            except NotImplementedError:
                continue

    async def delete(self, token: PipelineToken):
        '''Delete an object from the stores.'''
        for store in self.stores:
            try:
                await store.delete(token)
            except (NotImplementedError, NotFound):
                continue

    async def contains(self, token: PipelineToken):
        '''Check if an object exist in stores of type Cache.'''
        contains = False
        for store in self.stores:
            try:
                contains = await store.contains(token)
            except NotImplementedError:
                continue
            if contains: break
        return contains
