# Threading 

Module: `pyot.utils.threading` 

### _class_ `AsyncLock`

> An asynchronous threading Lock. The event loop won't be blocked when acquiring the lock.

Definitions: 
* `__aenter__` -> `bool` 
  * `args`: `None` 
* `__aexit__` -> `None` 
  * `args`: `None` 
* `__init__` -> `None` 

Methods: 
* _asyncmethod_ `acquire` -> `bool` 
  > Acquire the lock without locking the loop 
* _method_ `release` -> `None` 
  > Release the lock, this is not async because it is immediate and useful for hooks (e.g. registering `atexit`) 


