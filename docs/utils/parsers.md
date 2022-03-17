# Parsers 

Module: `pyot.utils.parsers` 

### _function_ `from_bytes` -> `~T` 
* `obj`: `bytes` 
* `class_of_t`: `Union[Type[~T], NoneType] = None` 
> Convert a byte string to python object. 


### _function_ `safejson` -> `Any` 
* `content`: `str` 
> Same as json.loads with graceful fallback by returning original string 


### _function_ `to_bytes` -> `bytes` 
* `obj`: `Any` 
> Convert a python object to byte string. 


