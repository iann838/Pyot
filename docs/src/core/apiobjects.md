# Objects

Pyot comes with a big number of API objects, each of them points to a different source of data, but one thing that doesn't change is their inherited class behavior. All attributes and methods should be available by IDE autocompletion. If you don't see autocompletion, there is a chance that you brrrr'd your code on the way. Below is a list of objects that is used for inheriting all the API objects.

## Pyot Core

* This object is identified using the badge <Badge text="Pyot Core" vertical="middle"/> in the API section.

This is main type of objects that developers works with. Below is a list of general member methods:

> ### `__init__(**kwargs)` <Badge text="Pyot Core" vertical="middle"/>
> Creates an instance of the Pyot Core Object. Parameters vary per API.

> ### `get(sid: str = None, pipeline: str = None, deepcopy: bool = False)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/> <Badge text="unchainable" type="warning" vertical="middle"/>
> Awaitable that executes `get` request to the pipeline, finds the requested data, returns it and sinks through the pipeline.
> - `sid` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the sid identifying the created session on the pipeline to reuse, typically session created by `Queue`.
> - `pipeline` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the name identifying the pipeline to execute on, typically only passed when used with objects of the RIOT model.
> - `deepcopy` <Badge text="param" type="warning" vertical="middle"/> <Badge text="New 3.0.0" type="error" vertical="middle"/>: Optional, flag to save raw response using `fast_copy` (True) or transformers smart copy (False). Defaults to False.
> - ~~`keep_raw`~~ <Badge text="param" type="warning" vertical="middle"/> <Badge text="Removed 3.0.0" type="error" vertical="middle"/>
> - ~~`ptr_cache`~~ <Badge text="param" type="warning" vertical="middle"/> <Badge text="Removed 3.0.0" type="error" vertical="middle"/>
> ::: danger DEPRECATED
> `keep_raw` and `ptr_cache` param removed since v3.0.0
> :::

> ### `post(sid: str = None, pipeline: str = None, deepcopy: bool = False)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/> <Badge text="unchainable" type="warning" vertical="middle"/>
> Awaitable that executes `post` request to the pipeline, finds the correct service to execute and return the response if given. Unlike `get()` responses are not sinked through the pipeline.
> * Parameters are the same of `get()`

> ### `put(sid: str = None, pipeline: str = None, deepcopy: bool = False)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/> <Badge text="unchainable" type="warning" vertical="middle"/>
> Awaitable that executes `put` request to the pipeline, finds the correct service to execute and return the response if given. Unlike `get()` responses are not sinked through the pipeline.
> * Parameters are the same of `get()`

> ### `query(**kwargs)` <Badge text="function" type="error" vertical="middle"/>
> Appends query parameters to the object, these are mostly query parameters specified in endpoints of Riot Dev Portal. Query parameters vary per object.

> ### `body(**kwargs)` <Badge text="function" type="error" vertical="middle"/>
> Adds the body parameters to the object as kwargs, these are mostly body specified in endpoints of Riot Dev Portal that supports POST, PUT requests. The kwargs are later converted to the necessary json to pass on the request.

> ### `create_token()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Creates a Pyot Pipeline Token that can make calls on the low level pipeline API. This can be useful for using high performance local `PtrCache` or manually calling pipeline methods.

> ### `dict(deepcopy=False, lazy_props=False, recursive=True)` <Badge text="function" type="error" vertical="middle"/>
> This method returns the python dictionary representation of the object. Description placeholder
> - `deepcopy` <Badge text="param" type="warning" vertical="middle"/>: Description placeholder.
> - `lazy_props` <Badge text="param" type="warning" vertical="middle"/>: Description placeholder.
> - `recursive` <Badge text="param" type="warning" vertical="middle"/>: Define if dictionary returned should be the Meta cached data or an exact same copy of the Pyot object by going recursive all the way down to the bottom of the object structure. Getting from the Meta cached data has a complexity of O(1), it has the same structure as the object with some exceptions: 1. Most keys are camelCased, 2. Some renamed keys are not reflected, 3. Some values that returns python builtin objects might return raw params (e.g. `creation: datetime` is returned as `gameStartTime: unix millis`), meanwhile setting this param to `True` will get the exact copy but as a dict with the cost of more time and memory complexity. Defaults to `False`.
> - ~~`remove_server`~~ <Badge text="param" type="warning" vertical="middle"/> <Badge text="Removed 3.0.0" type="error" vertical="middle"/>
> - ~~`pyotify`~~ <Badge text="param" type="warning" vertical="middle"/> <Badge text="Renamed 3.0.0" type="error" vertical="middle"/>

> ### ~~`json(pyotify=False, remove_server=True)`~~ <Badge text="function" type="error" vertical="middle"/>
> ::: danger DEPRECATED
> This method has been removed since v3.0.0.
> :::

> ### `raw()` <Badge text="function" type="error" vertical="middle"/>
> Returns the raw response saved on the requesting methods (get, put, post), by default the raw response is saved using smart copying which is non-destructive but can have changes on it, to get the exact raw response, pass `deepcopy=True` to the requesting methods.


## Pyot Static

* This object is identified using the badge <Badge text="Pyot Static" vertical="middle"/> in the API section

These are objects that are nested into the Pyot Core Objects, inheriting some partial functions of the Pyot Core. Below is a list of general member methods:

> ### `dict(deepcopy=False, lazy_props=False, recursive=True)` <Badge text="function" type="error" vertical="middle"/>
> This method returns the python dictionary representation of the object.
> - `deepcopy` <Badge text="param" type="warning" vertical="middle"/>: The dictionary returned will be a copy of itself, thus mutation will not affect object indirectly.
> - `lazy_props` <Badge text="param" type="warning" vertical="middle"/>: Execute all `lazy_property`'s of the object (recursively) before returning the dictionary.
> - `recursive` <Badge text="param" type="warning" vertical="middle"/>: Define if dictionary returned should be the Meta cached data or an exact same copy of the Pyot object by going recursive all the way down to the bottom of the object structure. Getting from the Meta cached data has a complexity of O(1), it has the same structure as the object with some exceptions: 1. Most keys are camelCased, 2. Some renamed keys are not reflected, 3. Some values that returns python builtin objects might return raw params (e.g. `creation: datetime` is returned as `gameStartTime: unix millis`), meanwhile setting this param to `True` will get the exact copy but as a dict with the cost of more time and memory complexity. Defaults to `False`.
> - ~~`remove_server`~~ <Badge text="param" type="warning" vertical="middle"/> <Badge text="Removed 3.0.0" type="error" vertical="middle"/>
> - ~~`pyotify`~~ <Badge text="param" type="warning" vertical="middle"/> <Badge text="Renamed 3.0.0" type="error" vertical="middle"/>

> ### `json(pyotify=False, remove_server=True)` <Badge text="function" type="error" vertical="middle"/>
> ::: danger DEPRECATED
> This method has been removed since v3.0.0.
> :::

## Pyot Container

* This object is identified using the badge <Badge text="Pyot Container" vertical="middle"/>

These objects are made for managing groups of objects to ease development. For example, if you need a better way to manage a deck returned by `lor.Match`, it will return a `lor.Deck` container with its own unique methods to manipulate the deck.

> Methods are different on each container class. Check each of the models' documentation.
