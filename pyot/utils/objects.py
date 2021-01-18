from datetime import datetime, timedelta
import pickle

from .common import thread_run


class PtrCache:
    '''
    A high performance mini local cache based on reference keeping.
    Be aware that this cache is NOT isolated, hence the performance difference from Omnistone.
    This cache will not copy the objects on get/put, modification to objects affects cached objects.
    '''
    objects: dict
    max_entries: int

    def __init__(self, expiration=60*60*3, max_entries=5000):
        self.objects = {}
        self.expiration = expiration
        self.max_entries = max_entries

    def get(self, name: str, func=None, lazy: bool = False):
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

    async def aget(self, name: str, coro=None, lazy: bool = False):
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

    def set(self, name: str, val, exp: int = None):
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


def ptr_cache(expiration=60*60*3, max_entries=5000):
    '''Create an PtrCache and return it.'''
    return PtrCache(expiration, max_entries)


class FrozenGenerator:
    '''
    Generator that isolates the original list by returning a copy of the object when iterated.
    Used for preventing memory leaks of self-filled objects with the price of more CPU time.
    '''

    def __init__(self, li):
        self.objects = li

    def __iter__(self):
        return (pickle.loads(pickle.dumps(obj)) for obj in self.objects)


def frozen_generator(li):
    '''Create a FrozenGenerator and return it.'''
    return FrozenGenerator(li)


class AutoData:

    def __init__(self, func, interval=60*60*3):
        self.interval = interval
        self.func = func
        self.data = None
        self.next_update = datetime.now()
        self.updating = False

    def get(self):
        if self.next_update < datetime.now() and not self.updating:
            self.updating = True
            self.data = self.func()
            self.updating = False
            self.next_update = datetime.now() + timedelta(seconds=self.interval)
        return self.data

    async def aget(self):
        if self.next_update < datetime.now() and not self.updating:
            self.updating = True
            self.data = await thread_run(self.func)
            self.updating = False
            self.next_update = datetime.now() + timedelta(seconds=self.interval)
        return self.data
