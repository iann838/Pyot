from threading import Lock
import asyncio


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
        '''Release the lock, this is not async due to ability for easier cleanups (e.g. registering `atexit`)'''
        self._lock.release()
