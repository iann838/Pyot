# Sync 

Module: `pyot.utils.sync` 

### _function_ `async_to_sync` -> `Callable[..., ~R]` 
* `func`: `Callable[..., Awaitable[~R]]` 
> Wraps `asyncio.run` on an async function making it sync callable. Can be used as decorator @async_to_sync 


