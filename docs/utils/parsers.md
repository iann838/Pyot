# Parsers 

Module: `pyot.utils.parsers` 

### _function_ `from_bytes` -> `~T` 
* `obj`: `None` 
* `class_of_t`: `Union[Type[~T], NoneType] = None` 
> Convert a byte string to python object. 


### _function_ `safejson` -> `None` 
* `content`: `str` 
> Same as json.loads with graceful fallback by returning original string 


### _function_ `to_bytes` -> `ByteString` 
* `obj`: `None` 
> Convert a python object to byte string. 


