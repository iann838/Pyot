# About

This module exposes a wide set of utils methods and objects **_highly_** helpful for development.

If you want to iterate for all the items in events, **_it would be innefficient_** doing `await event.item.get()` for every loop, even if it is cached, because Pyot's stores makes sure that any data is **_safe_** from any type of mutation, so stores will automatically copy the object before retrieving it, which adds up significant amount of CPU time. Solution would be a local cache that saves a reference to the object, one of the use case of a `PtrCache` from this module.

Or if you want to convert a champion key to champion id without the need of pulling an entire `Champion` object then the method `champion_id_by_key` is here for you. There is also others common tools like the frequently mentioned `loop_run`, `fast_copy` which are even useful outside of Pyot environment.

## Imports

The methods and objects are organized in submodules but most of them are importable at the root of this module. For example:
```python
from pyot.utils import PtrCache
from pyot.utils.objects import PtrCache
```
Both of these imports are valid, have your taste.

## Legend

-<Badge text="function" type="error" vertical="middle"/>: This is a function.

-<Badge text="awaitable" type="error" vertical="middle"/>: This is an awaitable.
