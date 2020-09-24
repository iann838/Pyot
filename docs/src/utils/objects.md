# Objects

:::warning
Asynchronous callbacks are only runable on a-prefixed methods, e.g. `aget`.
:::

Submodule: `objects`

## `ArrowCache`
> A high performance mini local cache based on reference keeping. Be aware that this cache is NOT isolated, hence the performance difference (This one is much faster) from Omnistone.
> ::: warning
> This cache will not copy the objects on get/put, modification to objects affects cached objects.
> :::
> ### `__init__(expiration=60*60*3, max_entries=2000)`
> - `expiration` <Badge text="param" type="warning" vertical="middle"/>: Expiration time of objects.
> - `max_entries` <Badge text="param" type="warning" vertical="middle"/>: Max number of objects before culling.
> ### `get(name: str, func = None)` <Badge text="function" type="error" vertical="middle"/>
> Get an object from the cache.
> - `func` <Badge text="param" type="warning" vertical="middle"/> will be called when provided and if object doesn't exist, put the returned value to the cache and return it.
> ### `aget(name: str, coro = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Async get an object from the cache.
> - `coro` <Badge text="param" type="warning" vertical="middle"/> will be awaited when provided and if object doesn't exist, put the returned value to the cache and return it. If the `coro` doesn't need to be awaited it will be closed and not raise warnings.
> ### `set(name: str, val)` <Badge text="function" type="error" vertical="middle"/>
> Put an object to the cache.
> ### `clear()` <Badge text="function" type="error" vertical="middle"/>
> Clear the cache.

## `CloneGenerator`
> Generator that isolates the original list by copying each iterated object. Used for preventing memory leaks of -filled objects with the price of more CPU time.
> ### `__init__(li)`
> - `li` <Badge text="param" type="warning" vertical="middle"/>: The original list
> ### `__iter__()`
> Generator based iter.

Submodule: `locks`

:::tip
All these locks are preferably used in a context manager with `async with` to safeguard acquire and release the lock.
:::

## `SealLock`
> An awaitable threading Lock. The event loop won't be blocked when acquiring the lock.
> ### `__init__()`
> Create the lock object.
> ### `acquire()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Acquire the lock without locking the loop
> ### `release()` <Badge text="function" type="error" vertical="middle"/>
> Release the lock, this is not async for the sake of easier cleanup (e.g. registering `atexit`)

## `RedisLock`
> An awaitable redis Lock. The event loop won't be blocked when acquiring the lock.
> ### `__init__(redi, name: str = "", sleep: int = 0.02, timeout:int = 5, blocking_timeout: int = 10, thread_local: bool = False)`
> - `redi` <Badge text="param" type="warning" vertical="middle"/>: Redis instance from `redis.Redis`.
> - `name` <Badge text="param" type="warning" vertical="middle"/>: Name of the lock to allow multiple locks.
> - `sleep` <Badge text="param" type="warning" vertical="middle"/>: Sleep time per loop.
> - `timeout` <Badge text="param" type="warning" vertical="middle"/>: Timeout of the lock.
> - `blocking_timeout` <Badge text="param" type="warning" vertical="middle"/>: Timeout for acquire the lock.
> - `thread_local` <Badge text="param" type="warning" vertical="middle"/>: Flag the lock to belong the current thread (other thread can't see it).
> ### `acquire()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Acquire the lock without locking the loop
> ### `release()` <Badge text="function" type="error" vertical="middle"/>
> Release the lock, this is not async for the sake of easier cleanup (e.g. registering `atexit`)

Submodule: `dicts`

:::tip INFO
For these dict to use the default coroutine, call `aget` instead of `get`.
:::

:::warning
For using functions as their default callback, if args and kwargs needs to be passed please wrap them in `functools.partial`.

For using coroutines as their default callback, please pass the coroutine as it (as a coroutine function and not as coroutine object) if args and kwargs needs to be passed please wrap them in `functools.partial`. This is needed because the same coroutine cannot be awaited more than once.
:::


## `MultiDefaultDict`
> A default dict that supports coroutines as default callback and multiple get and sets. This dict can be subcripted or assign key values using regular dict syntax.
> ### `__init__(default: Callable)`
> - `default` <Badge text="param" type="warning" vertical="middle"/>: Coroutine object, function or partial as default callback.
> ### `__getitem__(name: str)`
> Get an object
> ### `__setitem__(name: str, val: Any)`
> Set an object
> ### `get(name: str)` <Badge text="function" type="error" vertical="middle"/>
> Get an object
> ### `set(name: str, val: Any)` <Badge text="function" type="error" vertical="middle"/>
> Set an object
> ### `fget(name: str)` <Badge text="function" type="error" vertical="middle"/>
> Returns a tuple of arguments that can be unpacked for pipelining
> ### `fset(name: str, val: Any)` <Badge text="function" type="error" vertical="middle"/>
> Returns a tuple of arguments that can be unpacked for pipelining
> ### `aget(name: str)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Async get
> ### `aset(name: str, val: Any)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Async set
> ### `mget(li: List[str])` <Badge text="function" type="error" vertical="middle"/>
> Get many objects
> ### `mset(dic: Mapping[str, Any])` <Badge text="function" type="error" vertical="middle"/>
> Set many objects

## `RedisDefaultDict`
> A Default dict that is stored on redis server. This dict can be subcripted or assign key values using regular dict syntax.
> ### `__init__(, redi: redis.Redis, default: Callable, prefix: str = "")`
> - `redi` <Badge text="param" type="warning" vertical="middle"/>: Redis instance from `redis.Redis`
> - `prefix` <Badge text="param" type="warning" vertical="middle"/>: Prefix to use for storing on the redis db.
> - `default` <Badge text="param" type="warning" vertical="middle"/>: Coroutine object, function or partial as default callback.
> ### `__getitem__(name: str)`
> Get an object
> ### `__setitem__(name: str, val: Any)`
> Set an object
> ### `get(name: str)` <Badge text="function" type="error" vertical="middle"/>
> Get an object
> ### `set(name: str, val: Any)` <Badge text="function" type="error" vertical="middle"/>
> Set an object
> ### `fget(name: str)` <Badge text="function" type="error" vertical="middle"/>
> Returns a tuple of arguments that can be unpacked for pipelining
> ### `fset(name: str, val: Any)`
> Returns a tuple of arguments that can be unpacked for pipelining
> ### `aget(name: str)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Async get
> ### `aset(name: str, val: Any)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Async set
> ### `mget(li: List[str])` <Badge text="function" type="error" vertical="middle"/>
> Get many objects
> ### `mset(dic: Mapping[str, Any])` <Badge text="function" type="error" vertical="middle"/>
> Set many objects

:::warning
Avoid storing `None` on RedisDefaultDict as it will trigger the default callback everytime.
:::
