# Object

Each created pipeline can be accessed in a dictionary at the `pyot.conf.pipeline` module. The key of the pipeline is the name provided in the configuration, if the pipeline is set as default, model name can be used aswell.

```python
from pyot.conf.pipeline import pipelines

lol_pipeline = pipelines["lol"]
```

### _class_ `Pipeline`

Definitions:

* `__init__`
  - `model`: `str`
    > Model of belonging.
  - `name`: `str`
    > Name of pipeline.
  - `stores`: `List[Store]`
    > List of Stores to add on the pipeline.

* `__iter__`
  > Iterates over `stores`.

* `__getitem__`
  > Get store by index.

Attributes:

* `model`: `str`
* `name`: `str`
* `stores`: `List[StoreObject]`
* `sessions`: `ResourceTemplate[aiohttp.ClientSession]`

Methods:

* _async_ `get` -> `Any`
  - `token`: `PipelineToken`
    > Token identifying the data, created by `token()` on Pyot Core objects.

* _async_ `set` -> `None`
  - `token`: `PipelineToken`
    > Token identifying the data, created by `token()` on Pyot Core objects.
  - `value`: `Any`
    > Data to be stored in qualified stores.
  - `stop`: `Store = None`
    > The instance of the store that it should stop at (not sink further).

* _async_ `post` -> `Any`
  - `token`: `PipelineToken`
    > Token identifying the data, created by `token()` on Pyot Core objects.
  - `body` -> `Any`
    > Body of the request.

* _async_ `put` -> `Any`
  - `token`: `PipelineToken`
    > Token identifying the data, created by `token()` on Pyot Core objects.
  - `body` -> `Any`
    > Body of the request.

* _async_ `clear` -> `None`
  > Clear data in all stores.

* _async_ `expire` -> `None`
  > Expire data in all the stores, used for stores that cannot automatically expire data on its own.

* _async_ `delete` -> `None`
  - `token`: `PipelineToken`
    > Token identifying the data, created by `token()` on Pyot Core objects.

* _async_ `contains` -> `bool`
  - `token`: `PipelineToken`
    > Token identifying the data, created by `token()` on Pyot Core objects.

## Example

```python
from pyot.conf.pipeline import pipelines
from pyot.utils.runners import loop_run

async def clear_cache_lol():
    lol_pipeline = pipelines["lol"]
    await lol_pipeline.clear()

loop_run(clear_everything())
```
