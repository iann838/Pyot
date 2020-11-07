# Pipeline

Just gonna copy paste from [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) because no need to rephrase merely same thing twice:
> The data pipeline is the series of caches, databases, and data sources (such as the Riot API) that both provide and store data. Data sources provide data, while data sinks store data; we call both of these “data stores”. Some parts of the data pipeline are only data sources (for example, the Riot API), while others are both data sources and data sinks (for example, caches and databases). The data pipeline is a list of data stores, where the order the data stores specifies how data is pulled and stored (see the next paragraph). Usually faster data stores go at the beginning of the data pipeline.
>
> When data is queried, a query dictionary is constructed containing the information needed to uniquely identify an object in a data source (e.g. a `region` and `summoner.id` are required when querying for `Summoner` objects). This query is passed up the data pipeline through the data sources, and at each data source the data pipeline asks if that source can supply the requested object. If the source can supply the object (for example, if the object is in the database, or if the Riot API can send the object/data), it is returned. If the source does not supply the object, the next data source in the pipeline is queried. If no data source can provide an object for the query, a `datapipelines.NotFoundError` is thrown.
>
> After an object is returned by a data source, the object gets passed back down the pipeline. Any data sinks along the way store the object that was returned by the data source. In this way, the cache (which should be at the front of the data pipeline) will store any object that a database or the Riot API returned.

Same happens in Pyot: Creates a Token that passes through the pipeline trying to get the data in the order, gets the data and sink down again. In Pyot any caches, db, and data sources are called "Stores", **_stores orders in the settings matters because that is the order of how Pyot prioritizes lookup._**
Each model will have its own pipeline, this is needed to create isolated environments and session groups that is better to maintain.

# Low Level API

Each created pipeline can be accessed as a **_dictionary_** at ~~Pyot's root level~~(Removed since v1.1.0) the pipeline module. The keys are the models names **_in lower case_**.

```python{1}
from pyot.pipeline import pipelines

lol_pipe = pipelines["lol"]
```

This object is created per `Settings` instance created. Below is a list of methods for the **_low level Pyot Pipeline API (You should use this only in specific cases, most cases Pyot Core objects will automatically deal this for you)_**.

> ## `__init__(model:str, stores: List[Any])`
> Creates a pipeline object
> - `model` <Badge text="param" type="warning" vertical="middle"/> -> str: Name of the object.
> - `stores` <Badge text="param" type="warning" vertical="middle"/> -> List[StoreObject]: List of Stores to add on the pipeline.

> ## `initialize()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
>::: danger DEPRECATED
>Removed since v1.1.0, due to adding unnecessary delays on imports.
>:::

> ## `transform_key(store_cls, method, key, content)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
>::: danger DEPRECATED
>Removed since v1.1.0, concept not clear, the helper functions are now accessible on the `utils` module.
>:::

> ## `get(token: PipelineToken, sid: str = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Method that starts lookup on stores, internal used by `PyotCore` objects **_and automatically sinks the data through the pipeline, so `put()` is not necessary._**
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required
> - `sid` <Badge text="param" type="warning" vertical="middle"/> -> str: The sid identifying the session to reuse.
>
>::: warning DEPRECATED
>Removed since v1.1.0: the `filter` param, now `_filter` is called at pyot object level.
>:::

> ## `set(self, token: PipelineToken, value: Any, stop=None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required
> - `value` <Badge text="param" type="warning" vertical="middle"/> -> Any: The data value to be cached on the pipeline Stores of type <Badge text="Pyot Cache" vertical="middle" />. Required
> - `stop` <Badge text="param" type="warning" vertical="middle"/> -> PyotStoreObject: The instance of the store that it should stop (hence not sink further).
>
>::: warning DEPRECATED
> This method has been renamed from the original `put` since v1.1.0, it is a reserved method for pyot's future undisclosable implementation.
>:::

> ## `post(self, token: PipelineToken, body: Any, sid: str = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required
> - `body` <Badge text="param" type="warning" vertical="middle"/> -> Any: The data body to be used for requesting in Stores of type <Badge text="Pyot Service" vertical="middle" />. Required
> - `sid` <Badge text="param" type="warning" vertical="middle"/> -> str: The sid identifying the session to reuse.

> ## `put(self, token: PipelineToken, body: Any, sid: str = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required
> - `body` <Badge text="param" type="warning" vertical="middle"/> -> Any: The data body to be used for requesting in Stores of type <Badge text="Pyot Service" vertical="middle" />. Required
> - `sid` <Badge text="param" type="warning" vertical="middle"/> -> str: The sid identifying the session to reuse.

> ## `clear()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Clear all the stores of type <Badge text="Pyot Cache" vertical="middle" />.

> ## `expire()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Expire all the stores of type <Badge text="Pyot Cache" vertical="middle" /> that cannot actively expire objects.

> ## `delete(token: PipelineToken)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Delete a data from all the stores of type <Badge text="Pyot Cache" vertical="middle" />.
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required

> ## `contains(token: PipelineToken)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Return `True` if one of the stores contains the data.
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required

> ## `sessions: Mapping[str, Any]` <Badge text="property" type="error" vertical="middle"/>
> A dict that stores living session id to session instances, typically used by `Gatherer` and `Queue`, to add a new session do `x.sessions[your_session_id] = session` where `x` is the pipeline instance, `your_session_id` the key identifying the session and `session` the session instance.

## Example Usage

```python{4,5}
from pyot.pipeline import pipelines
from pyot.utils import loop_run

async def clear_everything():
    lol = pipelines["lol"]
    await lol.clear()

loop_run(clear_everything())
```