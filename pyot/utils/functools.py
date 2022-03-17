

from asyncio import iscoroutinefunction
from typing import Any, Awaitable, Callable, Generic, TypeVar


R = TypeVar("R")


class async_property(Generic[R]):
    '''
    Async equivalent of `property`, takes an async method and
    converts it to a property that returns an awaitable with the return value.

    Usage:
    ```python
    class A:
        @async_property
        async def b(self):
            ...
    a = A()
    await a.b
    ```
    '''
    name = None

    @classmethod
    def func(cls, instance: Any) -> Any:
        raise TypeError(
            f'Cannot use {cls.__class__.__name__} instance without calling '
            '__set_name__() on it.'
        )

    def __init__(self, func: Callable[..., Awaitable[R]], name=None):
        assert iscoroutinefunction(func), "Cannot use on non-async functions"
        self.real_func = func
        self.__doc__ = getattr(func, '__doc__')

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
            self.func = self.real_func
        elif name != self.name:
            raise TypeError(
                f"Cannot assign the same {self.__class__.__name__} to two different names "
                f"({self.name} and {name})."
            )

    def __get__(self, instance, cls=None) -> Awaitable[R]:
        if instance is None:
            return self
        return self.proxy(instance)

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    async def proxy(self, instance: Any) -> Awaitable[R]:
        res = await self.func(instance)
        return res


class async_cached_property(async_property, Generic[R]):
    '''
    Async equivalent of `functools.cached_property`, takes an async method and
    converts it to a cached property that returns an awaitable with the return value.

    Usage:
    ```python
    class A:
        @async_cached_property
        async def b(self):
            ...

    a = A()
    await a.b
    ```
    '''
    name = None

    def __init__(self, func: Callable[..., Awaitable[R]], name=None):
        assert iscoroutinefunction(func), "Cannot use on non-async functions"
        self.real_func = func
        self.once = False
        self.__doc__ = getattr(func, '__doc__')

    async def proxy(self, instance: Any) -> Awaitable[R]:
        if self.once:
            try:
                return instance.__dict__[self.name]
            except KeyError:
                pass
        self.once = True
        res = instance.__dict__[self.name] = await self.func(instance)
        return res
