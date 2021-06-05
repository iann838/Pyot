from threading import Lock
import asyncio

try: # Delay exception if aioredlock is not installed
    from aioredlock import Aioredlock
except ModuleNotFoundError as e:
    Aioredlock = e

from .eventloop import LoopSensitiveManager


class SealLock:
    '''
    An asynchronous threading Lock. The event loop won't be blocked when acquiring the lock.
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
    An asynchronous redis Lock. The event loop won't be blocked when acquiring the lock.
    '''
    def __init__(self, host: str, port: int, db: int, retry_count: int, retry_delay_min: float, retry_delay_max: float):
        if isinstance(Aioredlock, Exception):
            raise Aioredlock
        self._connections = [f"redis://{host}:{port}/{db}"]
        self.retry_count = retry_count
        self.retry_delay_min = retry_delay_min
        self.retry_delay_max = retry_delay_max
        self._lock_managers = LoopSensitiveManager(self._new_lock_manager)

    def _new_lock_manager(self):
        return Aioredlock(self._connections, self.retry_count, self.retry_delay_min, self.retry_delay_max)

    async def __call__(self, name: str, timeout: int = 10):
        return await (await self._lock_managers.get()).lock(name, lock_timeout=timeout)
