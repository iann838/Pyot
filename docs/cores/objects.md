# Objects

Pyot provides many models, each model contains Pyot classes, and these classes creates instances of Pyot objects. Different types of Pyot objects has different structure and functionalities.

Module: `pyot.core.objects`

{% hint style='info' %}
This page documents the bases of Pyot classes and objects, for reference of models, please go to **Models** section.
{% endhint %}

## Pyot Static

Base class: `PyotStaticBase`

Takes a Python data and serialize it into Python objects based on defined type hints of its subclass. Attributes may return other Pyot Static objects, these objects are initially not serialized, instead are assigned as instances of `PyotLazy`, these objects will only be serialized upon first access of the attribute.

{% hint style='info' %}
Some internal info has been hidden, to learn more please review source code instead.
{% endhint %}

### _class_ `PyotStaticBase`

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
  * `force_copy`: `bool = False`
    > Force make deep copy before returning, default to `False` for shallow copy.
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

### _class_ `PyotCoreBase`

Extends: `PyotStaticBase`

Methods:
* `using` -> `None`
  * `pipeline_name`: `str`
  > Set the pipeline used for request in this instance.
* `query` -> `Self`
  > Add query parameters to the request. This method is only present if the class accepts query parameters.
* `body` -> `Self`
  > Add body parameters to the request. This method is only present if the class requires body parameters.
* _async_ `token` -> `PipelineToken`
  > Create a pipeline token that identifies this object.
* _async_ `get` -> `Self`
  * `force_copy`: `bool = False`
  > Make a GET request to the pipeline.
  > - `force_copy`: Force make a deep copy on raw before serializing, default to `False` for smart copy (multi-level shallow copy).
* _async_ `post` -> `Self`
  * `force_copy`: `bool = False`
  > Make a POST request to the pipeline.
  > - `force_copy`: Force make a deep copy on raw before serializing, default to `False` for smart copy (multi-level shallow copy).
* _async_ `put` -> `Self`
  * `force_copy`: `bool = False`
  > Make a PUT request to the pipeline.
  > - `force_copy`: Force make a deep copy on raw before serializing, default to `False` for smart copy (multi-level shallow copy).
* `raw` -> `Any`
  > Returns the raw response of the request, by default smart copy is used, therefore there could be differences and should not be modified, a safer option is use `force_copy` flag to do deepcopy of the response at the cost of performance.
* _classmethod_ `load` -> `Self`
  * `raw`: `Any`
  > Return an instance of the class and load the submitted raw data.

## Pyot Utils

Base class: `PyotUtilBase`

This type of objects are meant to be utilities objects. The definition of this base class is empty, it is only used for generating documentations and possible usecases involving `isinstance`.

## Example

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
