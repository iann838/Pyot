# Sync 

Module: `pyot.utils.sync` 

### _function_ `async_to_sync` -> `Callable[..., ~R]` 
* `func`: `Callable[..., Awaitable[~R]]` 
> Wraps `asyncio.run` on an async function converting it into a blocking function. Can be used as decorator @async_to_sync 


### _function_ `sync_to_async` -> `Callable[..., Awaitable[~R]]` 
* `func`: `Callable[..., ~R]` 
> Wraps `asyncio.get_event_loop().run_in_executor` on a blocking function converting it into a Future. Can be used as decorator @sync_to_async 


