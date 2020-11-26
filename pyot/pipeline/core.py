from typing import List, Any, Dict, Callable
from aiohttp import ClientSession
import pickle
import asyncio
import aiohttp

from pyot.core.exceptions import NotFound, NotFindable
from .token import PipelineToken


class Pipeline:
    '''Pyot Pipeline object, backbone of the entire framework.'''

    def __init__(self, model: str, stores: List[Any]):
        self.model = model
        self.stores = stores
        self.sessions = {}

    async def get(self, token: PipelineToken, sid: str = None):
        '''Get an object from the stores.'''
        async with PipelineSession(self, sid) as session:
            found_in = None
            for store in self.stores:
                try:
                    response = await store.get(token, session=session)
                    found_in = store
                except (NotImplementedError, NotFound, NotFindable) as e:
                    if self.stores[-1] == store or store.store_type == "SERVICE" and isinstance(e, NotFound):
                        raise
                    continue
                break
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

    async def post(self, token: PipelineToken, body: Any, sid: str = None):
        '''Post an object to stores of type Service.'''
        async with PipelineSession(self, sid) as session:
            for store in self.stores:
                try:
                    response = await store.post(token, body, session=session)
                except (NotImplementedError, NotFound, NotFindable) as e:
                    if self.stores[-1] == store or store.store_type == "SERVICE" and isinstance(e, NotFound):
                        raise
                    continue
                break
        return response

    async def put(self, token: PipelineToken, body: Any, sid: str = None):
        '''Put an object to stores of type Service.'''
        async with PipelineSession(self, sid) as session:
            for store in self.stores:
                try:
                    response = await store.put(token, body, session=session)
                except (NotImplementedError, NotFound, NotFindable) as e:
                    if self.stores[-1] == store or store.store_type == "SERVICE" and isinstance(e, NotFound):
                        raise
                    continue
                break
        return response

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


class PipelineSession:
    '''Manages a Pipeline Session'''
    session: aiohttp.ClientSession

    def __init__(self, pipeline: Pipeline, sid: str):
        self.pipeline = pipeline
        self.sid = sid

    async def __aenter__(self) -> "PipelineSessionManager":
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) if self.sid is None else self.pipeline.sessions[self.sid]
        return self.session

    async def __aexit__(self, *args):
        if self.sid is None:
            await self.session.close()
