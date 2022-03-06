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

Attributes: 
* `states` -> `Dict[str, Dict[asyncio.events.AbstractEventLoop, bool]]` 


### _constant_ `factories`: `[]` 


### _alias_ `resource_manager` ~ `ResourceManager` 


