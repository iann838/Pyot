# Safejson 

Module: `pyot.utils.safejson` 

### _function_ `load` -> `Any` 
* `fp`: `Union[_io.FileIO, _io.BytesIO]` 
* `kwargs`: `None` 
> Same as json.load with graceful fallback by returning the read content as is 


### _function_ `loads` -> `Any` 
* `content`: `Union[str, bytes]` 
* `kwargs`: `None` 
> Same as json.loads with graceful fallback by returning the passed content as is 


