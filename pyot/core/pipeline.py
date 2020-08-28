from typing import List, Any, Dict, Callable
from dataclasses import dataclass
from .exceptions import NotFound
from aiohttp import ClientSession
import pickle
import asyncio
import aiohttp

def default_filter(response):
    return response

@dataclass
class PyotPipelineToken:
    server: str
    method: str
    params: Dict[str, Any]
    queries: Dict[str, Any]

    def __hash__(self):
        return hash((self.server, self.method, str(self.params), str(self.queries)))

    @property
    def stringify(self):
        return (self.server+self.method+str(self.params)+str(self.queries)).replace(" ", "_")

class PyotPipeline:
    def __init__(self, stores: List[Any]):
        self.stores = stores
        self.sessions = {}

    async def initialize(self):
        statements = []
        for store in self.stores:
            statements.append(store.initialize())
        await asyncio.gather(*statements, return_exceptions=False)

    async def transform_key(self, store_cls, method, key, content):
        for store in self.stores:
            if store.__class__ is store_cls:
                return store._endpoints.transform_key(method, key, content)
        raise RuntimeError("[Trace: PyotPipeline] FATAL: no key transformer found")

    async def get(self, token: PyotPipelineToken, filter: Callable = default_filter, session_id: str = None):
        response = dict()
        found_in = None
        session = aiohttp.ClientSession() if session_id is None else self.sessions[session_id]
        try:
            for store in self.stores:
                try:
                    response = await store.get(token, session=session)
                    found_in = store
                except (NotImplementedError, NotFound):
                    if self.stores[-1] == store:
                        raise
                    continue
                break
        except:
            if session_id is None: await session.close()
            raise
        finally:
            if session_id is None: await session.close()
        
        for store in self.stores:
            try:
                if store == found_in:
                    break
                await store.put(token, response)
            except NotImplementedError:
                continue
        return pickle.loads(pickle.dumps(filter(response)))
        # Using pickle for dict copying and maintaining cleanest of sinked data
        # Note: pickle is performing 8 times faster than copy.deepcopy

    async def put(self, token: PyotPipelineToken, value: Any):
        for store in self.stores:
            try:
                await store.put(token, value)
            except NotImplementedError:
                continue

    async def clear(self):
        for store in self.stores:
            try:
                await store.clear()
            except NotImplementedError:
                continue

    async def expire(self):
        for store in self.stores:
            try:
                await store.expire()
            except NotImplementedError:
                continue

    async def delete(self, token: PyotPipelineToken):
        for store in self.stores:
            try:
                await store.delete(token)
            except (NotImplementedError, NotFound):
                continue

    async def contains(self, token: PyotPipelineToken):
        contains = False
        for store in self.stores:
            try:
                contains = await store.contains(token)
            except NotImplementedError:
                continue
            if contains: break
        return contains
