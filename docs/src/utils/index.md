# About

This module exposes a wide set of utils methods and objects **_highly_** helpful for development.

For example if you want to iterate for all the items in events of `lol.MatchTimeline` and get its cost, then **_it would be very innefficient_** if you do `await event.item.get()` every time, even if it is cached on Omnistone, because Pyot's stores should be **_safe_** from any type mutation, so Omnistone will automatically copy the object before retrieving it, which adds up huge amount of CPU time. Solution would be a local cache that doesn't copy the objects but instead keeping an _arrow_ referencing the object, which is the use case of an `ArrowCache`.

Or if you want to convert a champion key to champion id without the need of pulling an entire `Champion` object then the method `champion_id_by_key` is here for you. There is also others common tools like the frequently mentioned `loop_run`, `fast_copy` which are even useful outside of Pyot environment.

## Imports

The methods and objects are organized in submodules but most of them are importable at the root of this module. For example:
```python
from pyot.utils import ArrowCache
from pyot.utils.objects import ArrowCache
```
Both of these imports are valid, have your taste.

## Legend

-<Badge text="function" type="error" vertical="middle"/>: This is a function.

-<Badge text="awaitable" type="error" vertical="middle"/>: This is an awaitable.
