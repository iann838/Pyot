# Time 

Module: `pyot.utils.time` 

### _asyncfunction_ `atimeit` -> `None` 
* `coro`: `None` 
* `iters`: `int = 1` 
* `concurrent`: `bool = True` 
> Coroutine. measures the running time of a coroutine.
> 
> Coroutines with arguments should be passed using `functools.partial`.
> `iters` may be passed to specify the amount of repeat executions.
> `concurrent` to allow concurrent running of coroutines. 


### _function_ `timeit` -> `None` 
* `func_or_coro`: `None` 
* `iters`: `int = 1` 
* `concurrent`: `bool = True` 
> Measures the running time of a function or coroutine.
> Functions/Coroutines with arguments should be passed using `functools.partial`.
> `iters` may be passed to specify the amount of repeat executions.
> `concurrent` to allow concurrent running of coroutines. 


