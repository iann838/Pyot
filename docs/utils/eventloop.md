# Eventloop 

Module: `pyot.utils.eventloop` 

### _class_ EventLoopFactory

> Factory for creating isolated copies of internal streams for each unique event loop.

Extends: 
* `Generic` 

Definitions: 
* `__del__` -> `None` 
* `__init__` -> `None` 
  * `factory`: `Callable[..., Union[~R1, Awaitable[~R2]]]` 
  * `callback`: `None` 
  * `max_loops`: `int = 128` 
  * `t`: `Type[~R1] = None` 
* `__new__` -> `None` 
  * `cls`: `None` 
  * `args`: `None` 
  * `kwds`: `None` 

Methods: 
* _asyncmethod_ `close` -> `None` 
  * `loop`: `None` 
* _asyncmethod_ `cull` -> `None` 
* _asyncmethod_ `get` -> `Union[~R1, ~R2]` 
  * `args`: `None` 
  * `kwargs`: `None` 

Attributes: 
* `loops` -> `Dict[asyncio.events.AbstractEventLoop, Union[~R1, ~R2]]` 


### _class_ ResourceManager

> Resource managers for event loops

Methods: 
* _classmethod_ `atomic` -> `Callable[..., Awaitable[~R]]` 
  * `async_func`: `Callable[..., Awaitable[~R]]` 
  > Wrap an async function with an atomic resource manager.
  > This manager tells where exactly resources will be used in an event loop and
  > does proper setups and cleanups of these resources.
  > 
  > Only one atomic manager may be in action at any moment in an event loop.
  > 
  > Usage: As decorators. 

Attributes: 
* `states` -> `Dict[str, Dict[asyncio.events.AbstractEventLoop, bool]]` 


### _constant_ `factories`: `[]` 


### _alias_ `resource_manager` ~ `ResourceManager` 


