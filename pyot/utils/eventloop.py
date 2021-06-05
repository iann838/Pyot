import asyncio
from typing import Generic, TypeVar, Type, Callable, Awaitable

T = TypeVar("T")


class LoopSensitiveManager(Generic[T]):

    def __init__(self, factory: Callable[..., Awaitable[T]], callback=None, max_loops: int = 128, t: Type[T] = None):
        from .locks import SealLock # Ahh avoid circular imports oops
        self.loops = {}
        self.lock = SealLock()
        self.factory = factory
        self.max_loops = max_loops
        self.callback = callback or (lambda x: x)

    async def get(self, *args, **kwargs) -> T:
        loop = asyncio.get_event_loop()
        try:
            return self.loops[loop]
        except KeyError:
            instance = self.factory(*args, **kwargs)
            if asyncio.iscoroutine(instance):
                self.loops[loop] = await instance
            else:
                self.loops[loop] = instance
            if len(self.loops) >= self.max_loops:
                async with self.lock:
                    if len(self.loops) >= self.max_loops:
                        await self.cull()
            return self.loops[loop]

    async def cull(self):
        closed = []
        for loop in self.loops:
            if loop.is_closed():
                closed.append(loop)
        for loop in closed:
            item = self.loops.pop(loop)
            called = self.callback(item)
            if asyncio.iscoroutine(called):
                await called

    def __del__(self):
        asyncio.run(self.cull())
