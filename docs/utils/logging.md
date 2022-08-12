# Logging 

Module: `pyot.utils.logging` 

### _class_ `LazyLogger`

> Lazy logger which its `log()` method will do nothing if level equals 0

Extends: 
* `logging.Logger` 
* `logging.Filterer` 

Definitions: 
* `__init__` -> `None` 
  * `name`: `None` 

Methods: 
* _method_ `log` -> `None` 
  * `level`: `None` 
  * `msg`: `None` 
  > Same as logging.Logger.log, with a new level (0) to skip logging. 


