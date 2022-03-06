import asyncio
from collections import defaultdict
from functools import wraps
from typing import Dict, Generic, List, TypeVar, Type, Callable, Awaitable, Union

from .locks import SealLock


R = TypeVar("R")
R1 = TypeVar("R1")
R2 = TypeVar("R2")


factories: List["EventLoopFactory"] = []


class ResourceManager:
    '''Resource managers for event loops'''

    states: Dict[str, Dict[asyncio.AbstractEventLoop, bool]] = {
        "atomic": defaultdict(bool)
    }

    @classmethod
    def atomic(cls, async_func: Callable[..., Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        '''
        Decorator.\n
        Wrap an async function with an atomic resource manager.
        Ensure proper management of internal streams and resources for the current event loop.\n
        Only one atomic manager at most may be in action at any moment in the event loop. 
        '''
        if not asyncio.iscoroutinefunction(async_func):
            raise TypeError(f"'{async_func}' is not an async function")
        @wraps(async_func)
        async def wrapper(*args, **kwargs):
            state = cls.states["atomic"][asyncio.get_event_loop()]
            if state:
                raise RuntimeError("Another atomic resource manager is already running in the event loop")
            cls.states["atomic"][asyncio.get_event_loop()] = True
            try:
                return await async_func(*args, **kwargs)
            finally:
                await asyncio.gather(*(factory.close() for factory in factories))
                cls.states["atomic"][asyncio.get_event_loop()] = False
        return wrapper


resource_manager = ResourceManager


class EventLoopFactory(Generic[R1, R2]):
    '''Factory for creating isolated copies of internal streams for each unique event loop.'''

    loops: Dict[asyncio.AbstractEventLoop, Union[R1, R2]]

    def __init__(self, factory: Callable[..., Union[R1, Awaitable[R2]]], callback=None, max_loops: int = 128, t: Type[R1] = None):
        self.loops = {}
        self.lock = SealLock()
        self.factory = factory
        self.max_loops = max_loops
        self.callback = callback or (lambda x: x)
        factories.append(self)

    async def get(self, *args, **kwargs) -> Union[R1, R2]:
        loop = asyncio.get_event_loop()
        if loop in self.loops:
            return self.loops[loop]
        async with self.lock:
            if loop in self.loops:
                return self.loops[loop]
            instance = self.factory(*args, **kwargs)
            if asyncio.iscoroutine(instance):
                self.loops[loop] = await instance
            else:
                self.loops[loop] = instance
            if len(self.loops) >= self.max_loops:
                await self.cull()
            return self.loops[loop]

    async def close(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        try:
            item = self.loops.pop(loop)
            called = self.callback(item)
            if asyncio.iscoroutine(called):
                await called
        except KeyError:
            return

    async def cull(self) -> None:
        closed = []
        for loop in self.loops:
            if loop.is_closed():
                closed.append(loop)
        for loop in closed:
            item = self.loops.pop(loop)
            called = self.callback(item)
            if asyncio.iscoroutine(called):
                await called

    def __del__(self) -> None:
        asyncio.run(self.cull())
