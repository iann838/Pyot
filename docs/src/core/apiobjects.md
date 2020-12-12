# Objects

Pyot comes with a big number of API objects, each of them points to a different source of data, but one thing that doesn't change is their inherited class behavior. All attributes and methods should be available by IDE autocompletion. If you don't see autocompletion, there is a chance that you brrrr'd your code on the way. Below is a list of objects that is used for inheriting all the API objects.

## Pyot Core

* This object is identified using the badge <Badge text="Pyot Core" vertical="middle"/> in the API section.

This is main type of objects that developers works with. Below is a list of general member methods:

> ### `__init__(**kwargs)` <Badge text="Pyot Core" vertical="middle"/>
> Creates an instance of the Pyot Core Object. Parameters vary per API.

> ### `get(sid: str = None, pipeline: str = None, keep_raw: bool = False, ptr_cache: PtrCache = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/> <Badge text="unchainable" type="warning" vertical="middle"/>
> Awaitable that executes `get` request to the pipeline, finds the requested data, returns it and sinks through the pipeline.
> - `sid` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the sid identifying the created session on the pipeline to reuse, typically session created by `Queue`.
> - `pipeline` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the name identifying the pipeline to execute on, typically only passed when used with objects of the RIOT model.
> - `keep_raw` <Badge text="param" type="warning" vertical="middle"/>: Optional, boolean flag for storing raw data of the request as a dictionary that is later accessible through `.raw()`, typically for third party libraries to comsume.
> - `ptr_cache` <Badge text="param" type="warning" vertical="middle"/>: Optional, Intercepts a PtrCache, usage details please refer to [PtrCache](/utils/objects.html#PtrCache).

> ### `post(sid: str = None, pipeline: str = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/> <Badge text="unchainable" type="warning" vertical="middle"/>
> Awaitable that executes `post` request to the pipeline, finds the correct service to execute and return the response if given. Unlike `get()` responses are not sinked through the pipeline.
> - `sid` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the sid identifying the created session on the pipeline to reuse, typically session created by `Queue`.
> - `pipeline` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the name identifying the pipeline to execute on, typically only passed when used with objects of the RIOT model.

> ### `put(sid: str = None, pipeline: str = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/> <Badge text="unchainable" type="warning" vertical="middle"/>
> Awaitable that executes `put` request to the pipeline, finds the correct service to execute and return the response if given. Unlike `get()` responses are not sinked through the pipeline.
> - `sid` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the sid identifying the created session on the pipeline to reuse, typically session created by `Queue`.
> - `pipeline` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the name identifying the pipeline to execute on, typically only passed when used with objects of the RIOT model.

> ### `query(**kwargs)` <Badge text="function" type="error" vertical="middle"/>
> Appends query parameters to the object, these are mostly query parameters specified in endpoints of Riot Dev Portal. Query parameters vary per object.

> ### `body(**kwargs)` <Badge text="function" type="error" vertical="middle"/>
> Adds the body parameters to the object as kwargs, these are mostly body specified in endpoints of Riot Dev Portal that supports POST, PUT requests. The kwargs are later converted to the necessary json to pass on the request.

> ### `create_token()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Creates a Pyot Pipeline Token that can make calls on the low level pipeline API. This can be useful for using high performance local `PtrCache` or manually calling pipeline methods.

> ### `set_session_id(id: str)` <Badge text="function" type="error" vertical="middle"/>
>::: danger DEPRECATED
>This method has been removed since v1.1.0, now is accessible through an argument on the `get()` method.
>:::

> ### `dict(pyotify=False, remove_server=True)` <Badge text="function" type="error" vertical="middle"/>
> This method returns the python dictionary representation of the object. This object does not strictly return the original data that the store responded with, for that please call `get()` with `keep_raw=True` and `raw()`.
> - `pyotify`<Badge text="param" type="warning" vertical="middle"/>: Define if dictionary returned should be the Meta cached data or an exact same copy of the Pyot object by going recursive all the way down to the bottom of the object structure. Getting from the Meta cached data has a complexity of O(1), it has the same structure as the object with some exceptions: 1. Most keys are camelCased, 2. Some renamed keys are not reflected, 3. Some values that returns python builtin objects might return raw params (e.g. `creation: datetime` is returned as `gameStartTime: unix millis`), meanwhile setting this param to `True` will get the exact copy but as a dict with the cost of more time and memory complexity. Defaults to `False`.
>
> - `remove_server`<Badge text="param" type="warning" vertical="middle"/>: This only affects if `pyotify` is set to True, by nature the Core object will pass down the server (`platform`, `region`, `locale`) info to the Static objects in order to make correct "bridges", by setting to `False` the dict will not remove the server info for each object. Defaults to `True`.

> ### `json(pyotify=False, remove_server=True)` <Badge text="function" type="error" vertical="middle"/>
> This method returns the json serialized representation of the object, it is a shorcut of the long typed `json.dumps(x.dict())` where `x` is the Pyot Object.
> - `pyotify`<Badge text="param" type="warning" vertical="middle"/>: Refer to above description of the params
>
> - `remove_server`<Badge text="param" type="warning" vertical="middle"/>: Refer to above description of the params

> ### `raw()` <Badge text="function" type="error" vertical="middle"/>
> This method returns the dictionary containing the raw data, only available if `keep_raw=True` was passed when calling `get()`, the difference from `dict()` is that this dictionary will contain the original data returned by the store without any type of serialization nor transformation.


## Pyot Static

* This object is identified using the badge <Badge text="Pyot Static" vertical="middle"/> in the API section

These are objects that are nested into the Pyot Core Objects, inheriting some partial functions of the Pyot Core. Below is a list of general member methods:


> ### `dict(pyotify=False, remove_server=True)` <Badge text="function" type="error" vertical="middle"/>
> This method returns a python dictionary of the object.
> - `pyotify`<Badge text="param" type="warning" vertical="middle"/>: Refer to Pyot Core description of the params
>
> - `remove_server`<Badge text="param" type="warning" vertical="middle"/>: Refer to Pyot Core description of the params

> ### `json(pyotify=False, remove_server=True)` <Badge text="function" type="error" vertical="middle"/>
> This method returns a json serialized object, it is a shorcut of the long typed `json.dumps(x.dict())` where `x` is the Pyot Object.
> - `pyotify`<Badge text="param" type="warning" vertical="middle"/>: Refer to Pyot Core description of the params
>
> - `remove_server`<Badge text="param" type="warning" vertical="middle"/>: Refer to Pyot Core description of the params

## Pyot Container

* This object is identified using the badge <Badge text="Pyot Container" vertical="middle"/>

These objects are made for managing groups of objects to ease development. For example, if you need a better way to manage a deck returned by `lor.Match`, it will return a `lor.Deck` container with its own unique methods to manipulate the deck.

> Methods are different on each container class. Check each of the models' documentation.

## Pyot Lazy

* This object is identified using the badge <Badge text="Pyot Lazy" vertical="middle"/>

These objects are made to prevent overhead on the both Pyot Core and Pyot Static objects. It prevents loading unnecessary objects, more specifically when the Core object gets data back to fill or when a Static object is called to fill. Nested objects are not filled directly, but instead create an instance of `PyotLazyObject` that contains the nested data. When the nested data is called or touched, `PyotLazyObject` proceeds to fill the next level and returns the nested object.

> No methods are intended for direct usage, if you want to override a method, check source code to do so.
