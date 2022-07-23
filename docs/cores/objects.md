# Objects

Pyot provides many models, each model contains Pyot classes, and these classes creates instances of Pyot objects. Different types of Pyot objects has different structure and functionalities.

Module: `pyot.core.objects`

{% hint style='info' %}
This page documents the bases of Pyot classes and objects, for information of models, please go to **Models** page.
{% endhint %}

## Pyot Static

Base class: `PyotStaticBase`

Takes a Python data and serialize it into Python objects based on defined type hints of its subclass. Attributes may return other Pyot Static objects, these objects are initially not serialized, instead are assigned as instances of `PyotLazy`, these objects will only be serialized upon first access of the attribute.

{% hint style='info' %}
Some internal info has been hidden, to learn more please review source code instead.
{% endhint %}

### _class_ PyotStaticBase

Metaclass: `PyotMetaClass`

Extends: `PyotRoutingBase`

Definitions:
* `__getitem__` -> `Any`
  > Supports `object[item]` syntax, by using this syntax instead of `object.item` will return the `.dict()` representation of `object.item`, useful for avoiding serialization of `object.item` beforehand if unwanted.

Attributes:
* `_meta`: `Self.Meta`

Properties:
* `region` -> `str`
* `platform` -> `str`
* `version` -> `str`
* `locale` -> `str`
* `metaroot` -> `PyotCoreBase`
  > Returns the root Pyot Core object which this object is child of.
* `metapipeline` -> `Pipeline`
  > Returns the pipeline of this object's class' model.

Methods: 
* _method_ `dict` -> `Dict`
  * `deepcopy`: `bool = False`
    > Make a deep copy before returning, False for shallow copy.
  * `lazy_props`: `bool = False`
    > True for loading all `lazy_property`s before returning, False otherwise.
  * `recursive`: `bool = False`
    > True for returning `rdict()` content instead.
  > Returns the Python dict that is used for serialization on this object.
* _method_ `rdict` -> `Dict`
  > Returns the Python representation of object by doing recursive walks on itself.

## Pyot Core

Base class: `PyotCoreBase`

Inherits all functionalities of `PyotStaticBase`. This type of objects has the ability to request for data on pipelines.

{% hint style='info' %}
Some internal info has been hidden, to learn more please review source code instead.
{% endhint %}

### _class_ PyotCoreBase

Extends: `PyotStaticBase`

Methods:
* `pipeline` -> `None`
  * `name`: `str`
  > Change the pipeline of this object to request data on.
* `query` -> `Self`
  * `**kwargs`
  > Add query parameters to the request. Typings are present if the class accepts query parameters.
* `body` -> `Self`
  * `**kwargs`
  > Add body parameters to the request. Typings are present if the class accepts body parameters.
* _async_ `token` -> `PipelineToken`
  > Create a pipeline token that identifies this object.
* _async_ `get` -> `Self`
  * `pipeline`: `str = None`
  * `deepcopy`: `bool = False`
  > Make a GET request to the pipeline.
  > - `pipeline`: Name of the pipeline to make request on, default to default pipeline.
  > - `deepcopy`: Make a deepcopy to the raw response before serializing, default to False, use smart copy (make limited levels of recursive shallow copies) instead.
* _async_ `post` -> `Self`
  * `pipeline`: `str = None`
  * `deepcopy`: `bool = False`
  > Make a POST request to the pipeline.
  > - `pipeline`: Name of the pipeline to make request on, default to default pipeline.
  > - `deepcopy`: Make a deepcopy to the raw response before serializing, default to False, use smart copy (make limited levels of recursive shallow copies) instead.
* _async_ `put` -> `Self`
  * `pipeline`: `str = None`
  * `deepcopy`: `bool = False`
  > Make a PUT request to the pipeline.
  > - `pipeline`: Name of the pipeline to make request on, default to default pipeline.
  > - `deepcopy`: Make a deepcopy to the raw response before serializing, default to False, use smart copy (make limited levels of recursive shallow copies) instead.
* `raw` -> `Any`
  > Returns the raw response of the request, by default smart copy is used, therefore there could be differences and should not be modified, a safer option is use `deepcopy` flag to do deepcopy of the response at the cost of performance.
* _classmethod_ `load` -> `Self`
  * `raw_data`: `Any`
  > Return an instance of the class and loads the raw data into the object.

## Pyot Utils

Base class: `PyotUtilBase`

This type of objects are meant to be utilities objects. The definition of this base class is empty, it is only used for generating documentations and possible usecases involving `isinstance`.

## Example Usage

Get ranked solo/duo match ids of the last 24 hours for a summoner by name and platform. Assuming model is activated and pipeline properly configured.

```python
from datetime import datetime, timedelta

from pyot.models import lol
from pyot.utils.lol.routing import platform_to_region


async def get_match_ids(name: str, platform: str) -> List[str]:
    summoner = await lol.Summoner(name=name, platform=platform).get()
    match_history = await lol.MatchHistory(
        puuid=summoner.puuid,
        region=platform_to_region(summoner.platform)
    ).query(
        count=100,
        queue=420,
        start_time=datetime.now() - timedelta(days=200)
    ).get()
    return match_history.ids
```
