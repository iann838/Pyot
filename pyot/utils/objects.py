from datetime import datetime, timedelta
import pickle


class PtrCache:
    '''
    A high performance mini local cache based on reference keeping.
    Be aware that this cache is NOT isolated, hence the performance difference from Omnistone.
    This cache will not copy the objects on get/put, modification to objects affects cached objects.
    '''
    objects: dict
    max_entries: int

    def __init__(self, expiration=60*60*3, max_entries=2000):
        self.objects = {}
        self.expiration = expiration
        self.max_entries = max_entries

    def get(self, name: str, func = None):
        '''
        Get an object from the cache.

        `func` will be called when provided and if object doesn't exist,
        put the returned value to the cache and return it.
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
        response = func()
        self.set(name, response)
        return response

    async def aget(self, name: str, coro = None):
        '''
        Async get an object from the cache.

        `coro` will be awaited when provided and if object doesn't exist,
        put the returned value to the cache and return it.
        If the `coro` doesn't need to be awaited it will be closed and not raise warnings.
        '''
        try:
            data = self.objects[name]
            if data[1] is not None and data[1] < datetime.now():
                del self.objects[name]
                raise KeyError(name)
            if coro:
                coro.close()
            return data[0]
        except KeyError:
            if coro is None:
                return None
        response = await coro
        self.set(name, response)
        return response

    def set(self, name: str, val):
        '''Put an object to the cache.'''
        if self.expiration >= 0:
            self.objects[name] = [val, datetime.now() + timedelta(seconds=self.expiration)]
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


def ptr_cache(expiration=60*60*3, max_entries=2000):
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
