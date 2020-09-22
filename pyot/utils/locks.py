from threading import Lock
from redis.lock import Lock as RLock
import asyncio


class SealLock:
    '''
    An awaitable threading Lock. The event loop won't be blocked when acquiring the lock.
    '''
    def __init__(self):
        self._lock = Lock()

    async def __aenter__(self, *args):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._lock.acquire)
        return self

    async def __aexit__(self, *args):
        self._lock.release()

    async def acquire(self):
        '''Acquire the lock without locking the loop'''
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._lock.acquire)
        return self

    def release(self):
        '''Release the lock, this is not async for the sake of easier cleanup (e.g. registering `atexit`)'''
        self._lock.release()


class RedisLock:
    '''
    An awaitable redis Lock. The event loop won't be blocked when acquiring the lock.
    '''
    def __init__(self, redi, name: str = "", sleep: int = 0.02, timeout:int = 5, blocking_timeout: int = 10, thread_local: bool = False):
        self._lock = RLock(redi, name, sleep=sleep, timeout=timeout, blocking_timeout=blocking_timeout, thread_local=thread_local)

    async def __aenter__(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._lock.acquire)
        return self

    async def __aexit__(self, *args):
        self._lock.release()

    async def acquire(self):
        '''Acquire the lock without locking the loop'''
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._lock.acquire)

    def release(self):
        '''Release the lock, this is not async for the sake of easier cleanup (e.g. registering `atexit`)'''
        self._lock.release()
