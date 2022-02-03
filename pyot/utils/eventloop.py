import asyncio
from typing import Generic, TypeVar, Type, Callable, Awaitable, Union


R1 = TypeVar("R1")
R2 = TypeVar("R2")


class LoopSensitiveManager(Generic[R1, R2]):
    '''Manager for managing internal streams and creates isolated copies of them based on their event loops.'''

    def __init__(self, factory: Callable[..., Union[R1, Awaitable[R2]]], callback=None, max_loops: int = 128, t: Type[R1] = None):
        from .locks import SealLock # Ahh avoid circular imports oops
        self.loops = {}
        self.lock = SealLock()
        self.factory = factory
        self.max_loops = max_loops
        self.callback = callback or (lambda x: x)

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
