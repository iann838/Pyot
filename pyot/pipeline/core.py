from typing import List, Any, Iterator
import aiohttp

from pyot.core.exceptions import NotFound, NotFindable, PyotException
from pyot.utils.eventloop import EventLoopFactory
from pyot.stores.base import Store

from .token import PipelineToken


class Pipeline:
    '''Pipeline containing a sequence of stores for request execution.'''

    def __init__(self, model: str, name: str, stores: List[Store]):
        self.model = model
        self.name = name
        self.stores = stores
        self.sessions = EventLoopFactory(
            factory=lambda: aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)),
            callback=lambda session: session.close()
        )

    def __iter__(self) -> Iterator[Store]:
        return iter(self.stores)

    def __getitem__(self, item):
        return self.stores[item]

    async def get(self, token: PipelineToken):
        '''Get an object from the stores.'''
        session = await self.sessions.get()
        found_in = None
        last_exc = NotFindable
        for store in self.stores:
            try:
                response = await store.get(token, session=session)
                found_in = store
            except (NotImplementedError, NotFindable):
                continue
            except PyotException as e:
                last_exc = e
                continue
            break
        else:
            raise last_exc
        await self.set(token, response, found_in)
        return response

    async def set(self, token: PipelineToken, value: Any, stop=None):
        '''Set an object to stores of type Cache.'''
        session = await self.sessions.get()
        for store in self.stores:
            if store is stop: break
            try:
                await store.set(token, value, session=session)
            except NotImplementedError:
                continue

    async def post(self, token: PipelineToken, body: Any):
        '''Post an object to stores of type Service.'''
        session = await self.sessions.get()
        last_exc = NotFindable
        for store in self.stores:
            try:
                response = await store.post(token, body, session=session)
            except (NotImplementedError, NotFindable):
                continue
            except PyotException as e:
                last_exc = e
                continue
            break
        else:
            raise last_exc
        return response

    async def put(self, token: PipelineToken, body: Any):
        '''Put an object to stores of type Service.'''
        session = await self.sessions.get()
        last_exc = NotFindable
        for store in self.stores:
            try:
                response = await store.put(token, body, session=session)
            except (NotImplementedError, NotFindable):
                continue
            except PyotException as e:
                last_exc = e
                continue
            break
        else:
            raise last_exc
        return response

    async def clear(self):
        '''Clear stores of type Cache.'''
        session = await self.sessions.get()
        for store in self.stores:
            try:
                await store.clear(session=session)
            except NotImplementedError:
                continue

    async def expire(self):
        '''Expire stores of type Cache that cannot dynamically expire.'''
        session = await self.sessions.get()
        for store in self.stores:
            try:
                await store.expire(session=session)
            except NotImplementedError:
                continue

    async def delete(self, token: PipelineToken):
        '''Delete an object from the stores.'''
        session = await self.sessions.get()
        for store in self.stores:
            try:
                await store.delete(token, session=session)
            except (NotImplementedError, NotFound):
                continue

    async def contains(self, token: PipelineToken) -> bool:
        '''Check if an object exist in stores of type Cache.'''
        session = await self.sessions.get()
        contains = False
        for store in self.stores:
            try:
                contains = await store.contains(token, session=session)
            except NotImplementedError:
                continue
            if contains: break
        return contains
