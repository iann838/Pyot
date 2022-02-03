from datetime import datetime, timedelta
from typing import TypeVar, Callable, Generic, Optional, Type


T = TypeVar("T")
R = TypeVar("R")


class PtrCache(Generic[T]):
    '''
    A high performance mini local cache based on reference keeping.
    Be aware that this cache is NOT isolated, hence the performance difference from Omnistone.
    This cache will not copy the objects on get/put, modification to objects affects cached objects.

    You can pass a class to instantiation param `class_of_t` for typing and autocompletion.
    '''
    objects: dict
    max_entries: int

    def __init__(self, expiration=60*60*3, max_entries=5000, class_of_t: Optional[Type[T]] = None):
        self.objects = {}
        self.expiration = expiration
        self.max_entries = max_entries

    def get(self, name: str, func=None, lazy: bool = False) -> T:
        '''
        Get an object from the cache.

        `func` will be called when provided and if object doesn't exist, set the returned value before returning.\n
        `lazy` flag if `func` needs to be called before running it, therefore achieve lazy eval during runtime.
        '''
        try:
            data = self.objects[name]
            if data[1] is not None and data[1] < datetime.now():
                del self.objects[name]
                raise KeyError(name)
            return data[0]
        except KeyError:
            if func is None:
                return None
        response = func()() if lazy else func()
        self.set(name, response)
        return response

    async def aget(self, name: str, coro=None, lazy: bool = False) -> T:
        '''
        Async get an object from the cache.

        `coro` will be awaited when provided and if object doesn't exist, set the returned value before returning.\n
        `lazy` flag if `coro` needs to be called before running it, therefore achieve lazy eval during runtime.\n

        If the `coro` doesn't need to be awaited it will be closed and not raise warnings.
        '''
        try:
            data = self.objects[name]
            if data[1] is not None and data[1] < datetime.now():
                del self.objects[name]
                raise KeyError(name)
            if not lazy and coro:
                coro.close()
            return data[0]
        except KeyError:
            if coro is None:
                return None
        response = (await coro()) if lazy else (await coro)
        self.set(name, response)
        return response

    def set(self, name: str, val: T, exp: int = None):
        '''Put an object to the cache.'''
        if exp is None:
            exp = self.expiration
        if exp >= 0:
            self.objects[name] = [val, datetime.now() + timedelta(seconds=exp)]
        else:
            self.objects[name] = [val, None]
        if len(self.objects) > self.max_entries:
            number = 0
            for key in self.objects:
                if number < self.max_entries/2:
                    del self.objects[key]
                    number += 1
                    continue
                break
        return name

    def clear(self):
        '''Clear the cache.'''
        self.objects = dict()


ptr_cache = PtrCache


class cached_property(Generic[R]):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.
    A cached property can be made out of an existing method:
    (e.g. ``url = cached_property(get_absolute_url)``).
    """
    name = None

    @staticmethod
    def func(instance) -> R: # pylint: disable=method-hidden
        raise TypeError(
            'Cannot use cached_property instance without calling '
            '__set_name__() on it.'
        )

    def __init__(self, func: Callable[..., R], name=None):
        self.real_func = func
        self.__doc__ = getattr(func, '__doc__')

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
            self.func = self.real_func
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." % (self.name, name)
            )

    def __get__(self, instance, cls=None) -> R:
        """
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res
