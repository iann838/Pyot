from typing import List, Any, Dict
from dataclasses import dataclass
from .exceptions import NotFound
from aiohttp import ClientSession
import asyncio


@dataclass
class PyotPipelineToken:
    server: str
    method: str
    params: Dict[str, Any]
    queries: Dict[str, Any]

    def __hash__(self):
        return hash((self.server, self.method, str(self.params), str(self.queries)))


class PyotPipeline:
    def __init__(self, stores: List[Any]):
        self.stores = stores

    async def initialize(self):
        statements = []
        for store in self.stores:
            statements.append(store.initialize())
        await asyncio.gather(*statements, return_exceptions=True)

    async def get(self, token: PyotPipelineToken):
        response = dict()
        found_in = None
        for store in self.stores:
            try:
                response = await store.get(token)
                found_in = store
            except (NotImplementedError, NotFound):
                if self.stores[-1] == store:
                    raise
                continue
            break
        for store in self.stores:
            try:
                if store == found_in:
                    continue
                await store.put(token, response)
            except NotImplementedError:
                continue
        return response

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
