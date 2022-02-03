# Cache 

Module: `pyot.utils.cache` 

### _class_ PtrCache

> A high performance mini local cache based on reference keeping.
> Be aware that this cache is NOT isolated, hence the performance difference from Omnistone.
> This cache will not copy the objects on get/put, modification to objects affects cached objects.
> 
> You can pass a class to instantiation param `class_of_t` for typing and autocompletion.

Extends: 
* `Generic` 

Definitions: 
* `__init__` -> `None` 
  * `expiration`: `int = 10800` 
  * `max_entries`: `int = 5000` 
  * `class_of_t`: `Union[Type[~T], NoneType] = None` 
* `__new__` -> `None` 
  * `cls`: `None` 
  * `args`: `None` 
  * `kwds`: `None` 

Methods: 
* _asyncmethod_ `aget` -> `~T` 
  * `name`: `str` 
  * `coro`: `None` 
  * `lazy`: `bool = False` 
  > Async get an object from the cache.
  > 
  > `coro` will be awaited when provided and if object doesn't exist, set the returned value before returning.
  > 
  > `lazy` flag if `coro` needs to be called before running it, therefore achieve lazy eval during runtime.
  > 
  > 
  > If the `coro` doesn't need to be awaited it will be closed and not raise warnings. 
* _method_ `clear` -> `None` 
  > Clear the cache. 
* _method_ `get` -> `~T` 
  * `name`: `str` 
  * `func`: `None` 
  * `lazy`: `bool = False` 
  > Get an object from the cache.
  > 
  > `func` will be called when provided and if object doesn't exist, set the returned value before returning.
  > 
  > `lazy` flag if `func` needs to be called before running it, therefore achieve lazy eval during runtime. 
* _method_ `set` -> `None` 
  * `name`: `str` 
  * `val`: `~T` 
  * `exp`: `int = None` 
  > Put an object to the cache. 

Attributes: 
* `objects` -> `dict` 
* `max_entries` -> `int` 


### _class_ cached_property

> Decorator that converts a method with a single self argument into a
> property cached on the instance.
> A cached property can be made out of an existing method:
> (e.g. ``url = cached_property(get_absolute_url)``).

Extends: 
* `Generic` 

Definitions: 
* `__get__` -> `~R` 
  * `instance`: `None` 
  * `cls`: `None` 
* `__init__` -> `None` 
  * `func`: `Callable[..., ~R]` 
  * `name`: `None` 
* `__new__` -> `None` 
  * `cls`: `None` 
  * `args`: `None` 
  * `kwds`: `None` 
* `__set_name__` -> `None` 
  * `owner`: `None` 
  * `name`: `None` 

Methods: 
* _method_ `func` -> `~R` 
  * `instance`: `None` 


### _alias_ `ptr_cache` ~ `PtrCache` 


