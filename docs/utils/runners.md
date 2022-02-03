# Runners 

Module: `pyot.utils.runners` 

### _function_ `loop_run` -> `~R` 
* `coro`: `Awaitable[~R]` 
> Run the coroutine in the current event loop or a new one if `set_event_loop()` has not yet been called. 


### _asyncfunction_ `thread_run` -> `~R` 
* `func`: `Callable[..., ~R]` 
* `args`: `None` 
* `kwargs`: `None` 
> Run a blocking function in a thread. 


