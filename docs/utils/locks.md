# Locks 

Module: `pyot.utils.locks` 

### _class_ SealLock

> An asynchronous threading Lock. The event loop won't be blocked when acquiring the lock.

Definitions: 
* `__aenter__` -> `None` 
  * `args`: `None` 
* `__aexit__` -> `None` 
  * `args`: `None` 
* `__init__` -> `None` 

Methods: 
* _asyncmethod_ `acquire` -> `None` 
  > Acquire the lock without locking the loop 
* _method_ `release` -> `None` 
  > Release the lock, this is not async due to ability for easier cleanups (e.g. registering `atexit`) 


