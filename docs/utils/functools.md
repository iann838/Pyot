# Functools 

Module: `pyot.utils.functools` 

### _class_ async_cached_property

> Async equivalent of `functools.cached_property`, takes an async method and
> converts it to a cached property that returns an awaitable with the return value.
> 
> Usage:
> ```
>     class A:
>         @async_cached_property
>         async def b(self):
>             ...
> 
>     a = A()
>     await a.b
> ```

Extends: 
* `pyot.utils.functools.async_property` 
* `Generic` 

Definitions: 
* `__get__` -> `Awaitable[~R]` 
  * `instance`: `None` 
  * `cls`: `None` 
* `__init__` -> `None` 
  * `func`: `Callable[..., Awaitable[~R]]` 
  * `name`: `None` 
* `__new__` -> `None` 
  * `cls`: `None` 
  * `args`: `None` 
  * `kwds`: `None` 
* `__set__` -> `None` 
  * `obj`: `None` 
  * `value`: `None` 
* `__set_name__` -> `None` 
  * `owner`: `None` 
  * `name`: `None` 

Methods: 
* _asyncmethod_ `proxy` -> `Awaitable[~R]` 
  * `instance`: `None` 


### _class_ async_property

> Async equivalent of `property`, takes an async method and
> converts it to a property that returns an awaitable with the return value.
> 
> Usage:
> ```
>     class A:
>         @async_property
>         async def b(self):
>             ...
> 
>     a = A()
>     await a.b
> ```

Extends: 
* `Generic` 

Definitions: 
* `__get__` -> `Awaitable[~R]` 
  * `instance`: `None` 
  * `cls`: `None` 
* `__init__` -> `None` 
  * `func`: `Callable[..., Awaitable[~R]]` 
  * `name`: `None` 
* `__new__` -> `None` 
  * `cls`: `None` 
  * `args`: `None` 
  * `kwds`: `None` 
* `__set__` -> `None` 
  * `obj`: `None` 
  * `value`: `None` 
* `__set_name__` -> `None` 
  * `owner`: `None` 
  * `name`: `None` 

Methods: 
* _asyncmethod_ `proxy` -> `Awaitable[~R]` 
  * `instance`: `None` 


