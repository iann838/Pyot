
from typing import Any, Dict, Generic, List, Set, TypeVar, Callable, Awaitable, Union
import asyncio
import functools
import inspect
import warnings

from pyot.utils.threading import AsyncLock

from .warnings import PyotResourceWarning


R = TypeVar("R")
F = TypeVar("F", bound=Callable)


resource_managed_loops: Set[asyncio.AbstractEventLoop] = set()
resource_templates: List["ResourceTemplate"] = []


class ResourceManager:
    '''
    Ensures acquisition and releasing of resources used by Pyot.
    - `exist_ok`: > If another resource manager is currently active in the event loop, skip this context,
    avoid using this flag unless unavoidable.
    '''

    def __init__(self, exist_ok: bool = False) -> None:
        self._skip_context = False
        self.loop = asyncio.get_event_loop()
        self.exist_ok = exist_ok

    async def __aenter__(self) -> "ResourceManager":
        current_loop = asyncio.get_event_loop()
        if self.loop != current_loop:
            raise RuntimeError(f"Resource manager bound to event loop {id(self.loop)} cannot acquire using event loop {id(current_loop)}")
        if self.loop in resource_managed_loops:
            if not self.exist_ok:
                raise RuntimeError(f"Event loop {id(self.loop)} already has an active resource manager")
            self._skip_context = True
        else:
            resource_managed_loops.add(self.loop)
            for template in resource_templates:
                await template.acquire(self.loop)
        return self

    async def __aexit__(self, *args) -> None:
        if self._skip_context:
            self._skip_context = False
        else:
            resource_managed_loops.remove(self.loop)
            for template in resource_templates:
                await template.release(self.loop)

    @classmethod
    def as_decorator(cls, func: F) -> F:
        if not inspect.iscoroutinefunction(func):
            raise TypeError(f"{func} is not a coroutine function")
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with cls():
                return await func(*args, **kwargs)
        return wrapper

    async def acquire(self):
        return await self.__aenter__()

    async def release(self):
        return await self.__aexit__()


resource_manager = ResourceManager


class ResourceTemplate(Generic[R]):
    '''
    Template for acquiring resources bound to event loops.

    - `acquire_func`: Function for acquiring the resource, the return value will be awaited if it is a coroutine.
    - `release_func`: Function for releasing the resource, the return value will be awaited if it is a coroutine. Optional.

    The submitted functions **must not implement locks**, it may cause deadlocks
    because the acquisition and releasing process are also behind a lock.
    '''

    _acquisitions: Dict[asyncio.AbstractEventLoop, R]

    def __init__(self, acquire_func: Callable[[], Union[R, Awaitable[R]]], release_func: Callable[[R], Any] = None) -> None:
        self._acquisitions = {}
        self._lock = AsyncLock()
        self.acquire_func = acquire_func
        self.release_func = release_func
        resource_templates.append(self)

    async def acquire(self, loop: asyncio.AbstractEventLoop = None) -> R:
        if loop is None:
            loop = asyncio.get_event_loop()
        if loop in self._acquisitions:
            return self._acquisitions[loop]
        async with self._lock:
            if loop in self._acquisitions:
                return self._acquisitions[loop]
            instance = self.acquire_func()
            if inspect.isawaitable(instance):
                self._acquisitions[loop] = await instance
            else:
                self._acquisitions[loop] = instance
            if len(self._acquisitions) > 1 and loop not in resource_managed_loops:
                warnings.warn(
                    f"Multithreading detected but event loop {id(loop)} is not using a resource manager, "
                    "acquired resources by this event loop will not be able to release gracefully.",
                    PyotResourceWarning
                )
            if len(self._acquisitions) % 32 == 0:
                await self.purge()
            return self._acquisitions[loop]

    async def release(self, loop: asyncio.AbstractEventLoop = None):
        if loop is None:
            loop = asyncio.get_event_loop()
        async with self._lock:
            try:
                acquisition = self._acquisitions.pop(loop)
                if self.release_func is not None:
                    called = self.release_func(acquisition)
                    if inspect.isawaitable(called):
                        await called
            except KeyError:
                raise ValueError(f"Acquisition not found for event loop {id(loop)}")

    async def purge(self) -> None:
        '''Purge acquired resources for all closed loops. Ungraceful release.'''
        closed_loops = []
        for loop in self._acquisitions:
            if loop.is_closed():
                closed_loops.append(loop)
        await asyncio.gather(*(self.release(closed_loop) for closed_loop in closed_loops))
