from typing import Callable, Any, List, Mapping
from collections import defaultdict
from functools import partial
import asyncio
import redis
import pickle


class MultiDefaultDict:
    '''A default dict that supports coroutines as default callback and multiple get and sets.\n
    This dict can be subcripted or assign key values using regular dict syntax.\n
    Methods: `get`, `set`, `aget`, `aset`, `mget`, `mset`, `fget`, `fset`.
    '''

    def __init__(self, default: Callable = None):
        self.default = default
        if default:
            self._object = defaultdict(default)
        else:
            self._object = defaultdict()

    def __getitem__(self, name: str):
        '''Get an object.'''
        return self._object[name]

    def __setitem__(self, name: str, val: Any):
        '''Set an object.'''
        self._object[name] = val
        return True

    def get(self, name: str):
        '''Get an object.'''
        return self.__getitem__(name)

    def set(self, name: str, val: Any):
        '''Set an object.'''
        return self.__setitem__(name, val)

    def fget(self, name: str):
        '''returns a tuple of arguments that can be unpacked for pipelining'''
        return (name,)

    def fset(self, name: str, val: Any):
        '''returns a tuple of arguments that can be unpacked for pipelining'''
        return (name, val,)

    async def aget(self, name: str):
        '''Async get'''
        val = self._object[name]
        if not asyncio.iscoroutine(val):
            return val
        val = await self.default
        await self.aset(name, val)
        return val

    async def aset(self, name: str, val: Any):
        '''Async set'''
        self._object[name] = val
        return True

    def mget(self, li: List[str]):
        '''Get many objects'''
        return [self.__getitem__(item) for item in li]

    def mset(self, dic: Mapping[str, Any]):
        '''Set many objects'''
        for key, val in dic.items():
            self.__setitem__(key, val)
        return True


def multi_defaultdict(default: Callable = None):
    '''Create a MultiDefaultDict and return it.'''
    return MultiDefaultDict(default)


class RedisDefaultDict:
    '''A Default dict that is stored on redis server.\n
    This dict can be subcripted or assign key values using regular dict syntax.\n
    Methods: `__getitem__`, `__setitem__`, `get`, `set`, `aget`, `aset`, `mget`, `mset`, `fget`, `fset`.
    '''
    
    def __init__(self, redi: redis.Redis, default: Callable = None, prefix: str = ""):
        self._redis = redi
        self._prefix = prefix
        self.default = default

    def __getitem__(self, name: str):
        val = self._redis.get(f'{self._prefix}{name}')
        if val is not None:
            return pickle.loads(val)
        if self.default is None: raise KeyError(name)
        val = self.default()
        self.set(name, val)
        return val

    def __setitem__(self, name: str, val: Any):
        return self._redis.set(f'{self._prefix}{name}', pickle.dumps(val, protocol=-1))

    def get(self, name: str):
        return self.__getitem__(name)

    def set(self, name: str, val: Any):
        return self.__setitem__(name, val)

    def fget(self, name: str):
        '''returns a tuple of arguments that can be unpacked for pipelining'''
        return (f'{self._prefix}{name}',)

    def fset(self, name: str, val: Any):
        '''returns a tuple of arguments that can be unpacked for pipelining'''
        return (f'{self._prefix}{name}', pickle.dumps(val, protocol=-1))

    async def aget(self, name: str):
        '''Async get'''
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(None, partial(self.__getitem__, f'{self._prefix}{name}'))
        if resp: return resp
        if self.default is None: raise KeyError(name)
        val = await self.default()
        await self.aset(name, val)
        return val

    async def aset(self, name: str, val: Any):
        '''Async set'''
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self.__setitem__, f'{self._prefix}{name}', pickle.dumps(val, protocol=-1)))

    def mget(self, li: List[str]):
        '''Get many objects'''
        keys = [f'{self._prefix}{name}' for name in li]
        try:
            return [pickle.loads(val) if val is not None else self.default() for val in self._redis.mget(keys)]
        except Exception:
            raise KeyError(li)

    def mset(self, dic: Mapping[str, Any]):
        '''Set many objects'''
        mapping = {}
        for name, val in dic.items():
            mapping[f'{self._prefix}{name}'] = pickle.dumps(val, protocol=-1)
        return self._redis.mset(mapping)


def redis_defaultdict(redi: redis.Redis, default: Callable = None, prefix: str = ""):
    '''Create a RedisDefaultDict and return it.'''
    return RedisDefaultDict(redi, default, prefix)
