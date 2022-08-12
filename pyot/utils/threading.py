from threading import Lock
import asyncio


class AsyncLock:
    '''
    An asynchronous threading Lock. The event loop won't be blocked when acquiring the lock.
    '''
    def __init__(self):
        self._lock = Lock()

    async def __aenter__(self, *args) -> bool:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._lock.acquire)

    async def __aexit__(self, *args):
        self._lock.release()

    async def acquire(self) -> bool:
        '''Acquire the lock without locking the loop'''
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._lock.acquire)

    def release(self):
        '''Release the lock, this is not async because it is immediate and useful for hooks (e.g. registering `atexit`)'''
        self._lock.release()
