from threading import Lock
import asyncio


class PyotLock():
    def __init__(self):
        self._lock = Lock()

    async def __aenter__(self, *args):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._lock.acquire)
        return self

    async def __aexit__(self, *args):
        self._lock.release()