# Sync 

Module: `pyot.utils.sync` 

### _function_ `async_to_sync` -> `Callable[..., ~R]` 
* `func`: `Callable[..., Awaitable[~R]]` 
> Wraps `asyncio.run` on an async function converting to sync callable. Can be used as decorator @async_to_sync 


### _function_ `sync_to_async` -> `Callable[..., Awaitable[~R]]` 
* `func`: `Callable[..., ~R]` 
> Wraps `thread_run` on a blocking function converting to async by running in a thread. Can be used as decorator @sync_to_async 


