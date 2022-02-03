# Eventloop 

Module: `pyot.utils.eventloop` 

### _class_ LoopSensitiveManager

> Manager for managing internal streams and creates isolated copies of them based on their event loops.

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
* _asyncmethod_ `cull` -> `None` 
* _asyncmethod_ `get` -> `Union[~R1, ~R2]` 
  * `args`: `None` 
  * `kwargs`: `None` 


