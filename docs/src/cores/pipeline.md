# Pipeline

Just gonna copy paste from [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) because no need to rephrase merely same thing twice:
> The data pipeline is the series of caches, databases, and data sources (such as the Riot API) that both provide and store data. Data sources provide data, while data sinks store data; we call both of these “data stores”. Some parts of the data pipeline are only data sources (for example, the Riot API), while others are both data sources and data sinks (for example, caches and databases). The data pipeline is a list of data stores, where the order the data stores specifies how data is pulled and stored (see the next paragraph). Usually faster data stores go at the beginning of the data pipeline.
>
> When data is queried, a query dictionary is constructed containing the information needed to uniquely identify an object in a data source (e.g. a `region` and `summoner.id` are required when querying for `Summoner` objects). This query is passed up the data pipeline through the data sources, and at each data source the data pipeline asks if that source can supply the requested object. If the source can supply the object (for example, if the object is in the database, or if the Riot API can send the object/data), it is returned. If the source does not supply the object, the next data source in the pipeline is queried. If no data source can provide an object for the query, a `datapipelines.NotFoundError` is thrown.
>
> After an object is returned by a data source, the object gets passed back down the pipeline. Any data sinks along the way store the object that was returned by the data source. In this way, the cache (which should be at the front of the data pipeline) will store any object that a database or the Riot API returned.

Same happens in Pyot: Creates a Token that passes through the pipeline trying to get the data in the order, gets the data and sink down again. In Pyot any caches, db, and data sources are called "Stores", **_stores orders in the settings matters because that is the order of how Pyot prioritizes lookup._**
Each model will have its own pipeline, this is needed to create isolated environments and session groups that is better to maintain.

## Pyot Pipeline Low Level API

Each created pipeline can be accessed as a **_dictionary_** at Pyot's root level. The keys are the models names **_in lower case_**.

```python{1,4}
import pyot
lol = pyot.pipelines["lol"]
# OR
from pyot import pipelines
lol = pipelines["lol"]
```

This object is created per `Settings` instance created. Below is a list of methods for the **_low level Pyot Pipeline API (You should use this only in specific cases, most cases Pyot Core objects will automatically deal this for you)_**.

> ### `__init__(stores: List[Any])`
> Creates a pipeline object, only intended to internal use

> ### `initialize()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Initializes the all the stores in the pipeline if it needs, **_This is automatic and you should see a warning log per pipeline creation_**.

> ### `transform_key(store_cls, method, key, content)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Transforms a needed `load` from provided content, internal used by `PyotCore` objects.
> - `store_cls`<Badge text="param" type="warning" vertical="middle"/> -> `Any`: The class of the Store, it can be imported from `pyot.stores`.
>
> - `method`<Badge text="param" type="warning" vertical="middle"/> -> `str`: The Pyot Pipeline method key (e.g. `"summoner_v4_by_name"`)
>
> - `key` <Badge text="param" type="warning" vertical="middle"/> -> `str`: The wanted load name.
>
> - `content` <Badge text="param" type="warning" vertical="middle"/> -> `Any`: The provided content.

> ### `get(token: PyotPipelineToken, filter: Callable = default_filter, session_id: str = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Method that starts lookup on stores, internal used by `PyotCore` objects **_and automatically sinks the data through the pipeline, so `put()` is not necessary._**
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PyotPipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required
>
> - `filter` <Badge text="param" type="warning" vertical="middle"/> -> Callable: A function that receives 1 argument data and returns the needed data, defaults to a function `def default_filter(response): return response`.

> ### `put(self, token: PyotPipelineToken, value: Any)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PyotPipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required
> - `value` <Badge text="param" type="warning" vertical="middle"/> -> Any: The data body to be `put` on the pipeline Stores. Required

> ### `clear()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Clear all the stores of type <Badge text="Pyot Cache" vertical="middle" />.

> ### `expire()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Expire all the stores of type <Badge text="Pyot Cache" vertical="middle" />.

> ### `delete(token: PyotPipelineToken)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Delete a data from all the stores of type <Badge text="Pyot Cache" vertical="middle" />.
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PyotPipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required

> ### `contains(token: PyotPipelineToken)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Return `True` if one of the stores contains the data.
> - `token` <Badge text="param" type="warning" vertical="middle"/> -> PyotPipelineToken: The token to use for identifying the data, created using `create_token()` on Pyot Core objects. Required

> ### `sessions: Mapping[str, Any]` <Badge text="property" type="error" vertical="middle"/>
> A dict that stores living session id to session instances, typically used by Pyot Gatherer, to add a new session just do `x.sessions[your_session_id] = session` where `x` is the pipeline instance, `your_session_id` the key identifying the session and `session` the session instance.

## Example Usage

```python{4,5}
from pyot import pipelines

async def clear_everything():
    lol = pipelines["lol"]
    await lol.clear()

pyot.run(clear_everything())
```