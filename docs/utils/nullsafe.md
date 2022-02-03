# Nullsafe 

Module: `pyot.utils.nullsafe` 

### _class_ NullSafe

> Documentation at: https://github.com/paaksing/nullsafe-python

Definitions: 
* `__bool__` -> `None` 
* `__call__` -> `NullSafe` 
  * `args`: `Any` 
  * `kwds`: `Any` 
* `__eq__` -> `bool` 
  * `o`: `object` 
* `__getattr__` -> `NullSafe` 
  * `k`: `str` 
* `__getitem__` -> `NullSafe` 
  * `k`: `str` 
* `__iter__` -> `None` 
* `__repr__` -> `str` 
* `__setattr__` -> `None` 
  * `name`: `str` 
  * `value`: `Any` 
* `__str__` -> `str` 


### _class_ NullSafeProxy

Extends: 
* `Generic` 

Definitions: 
* `__getattr__` -> `Union[Any, pyot.utils.nullsafe.NullSafe]` 
  * `name`: `str` 
* `__getitem__` -> `Union[Any, pyot.utils.nullsafe.NullSafe]` 
  * `k`: `str` 
* `__init__` -> `None` 
  * `o`: `~T` 
* `__new__` -> `None` 
  * `cls`: `None` 
  * `args`: `None` 
  * `kwds`: `None` 
* `__repr__` -> `str` 
* `__setattr__` -> `None` 
  * `name`: `str` 
  * `value`: `Any` 
* `__str__` -> `str` 


### _alias_ `_` ~ `nullsafe` 


### _function_ `nullsafe` -> `Union[~T, pyot.utils.nullsafe.NullSafe, pyot.utils.nullsafe.NullSafeProxy[~T]]` 
* `o`: `~T` 


### _constant_ `undefined`: `undefined` 


