# Objects

Pyot comes with a big number of API objects, each of them points to a different source of data, but one thing that doesn't change is their inherited class behavior, all attributes and methods should be available by IDE autocompletion, if you don't see it, there is a chance that you brrrr your code in the way. Below is a list of objects that is used for inheriting all the API objects.

## Pyot Core

* This object is identified using the badge <Badge text="Pyot Core" vertical="middle"/> in the API section

This is main type of objects that developers works with. Below is a list of general member methods:

> ### `__init__(**kwargs)` <Badge text="Pyot Core" vertical="middle"/>
> Creates an instance of the Pyot Core Object. Parameters varies per API.

> ### `get()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/> <Badge text="unchainable" type="warning" vertical="middle"/>
> This is an awaitable that makes a `get` to the pipeline, searching for what it needs and returns the found data.
> - `sid` <Badge text="param" type="warning" vertical="middle"/>: Optional, provide the sid identifying the created session on the pipeline to reuse, typically session created by `Queue`.

> ### `query(**kwargs)` <Badge text="function" type="error" vertical="middle"/>
> Appends query parameters to the object, these are normally the needed query parameters specified in Riot API Dev Portal. Parameters varies per object.

> ### `create_token()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Creates a Pyot Pipeline Token that can make calls on the low level pipeline API, this can be useful for using high performance local `ArrowCache` or manually calling pipeline methods.

> ### `set_session_id(id: str)` <Badge text="function" type="error" vertical="middle"/>
>::: danger DEPRECATED
>This method has been removed since v1.1.0, now is accessible through an argument on the `get()` method.
>:::

> ### `dict(pyotify=False, remove_server=True)` <Badge text="function" type="error" vertical="middle"/>
> This method returns a python dictionary of the object.
> - `pyotify`<Badge text="param" type="warning" vertical="middle"/>: Define if dictionary returned should be the Meta cached data or an exact same copy of the Pyot object by going recursive all the way down to the bottom of the object structure. Getting from the Meta cached data has a complexity of O(1), it has the same structure as the object with some exceptions: 1. Most keys are camelCased, 2. Some renamed keys are not reflected, 3. Some values that returns python builtin objects might return raw params (e.g. `creation: datetime` is returned as `gameStartTime: unix millis`), meanwhile setting this param to `True` will get the exact copy but as a dict with the cost of more time and memory complexity. Defaults to `False`.
>
> - `remove_server`<Badge text="param" type="warning" vertical="middle"/>: This only affects if `pyotify` is set to True, by nature the Core object will pass down the server (`platform`, `region`, `locale`) info to the Static objects in order to make correct "bridges", by setting to `False` the dict will not remove the server info for each object. Defaults to `True`.

> ### `json(pyotify=False, remove_server=True)` <Badge text="function" type="error" vertical="middle"/>
> This method returns a json serialized object, it is a shorcut of the long typed `json.dumps(x.dict())` where `x` is the Pyot Object.
> - `pyotify`<Badge text="param" type="warning" vertical="middle"/>: Refer to above description of the params
>
> - `remove_server`<Badge text="param" type="warning" vertical="middle"/>: Refer to above description of the params

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

## Pyot Lazy

* This object is identified using the badge <Badge text="Pyot Lazy" vertical="middle"/>

These objects are made to prevent overhead on the both Pyot Core and Pyot Static objects, it prevents loading unnecessary objects, more specifically when the Core object gets data back to _fill_ or when a Static object is called to _fill_, nested objects are _not_ filled directly, but creates an instance of `PyotLazyObject` that contains the nested data, and then when the nested data is needed or called, `PyotLazyObject` then proceeds to fill the next nested level object and returns the nested object.

> No methods are intended for direct usage, if you want to override a method, check source code to do so.