# About

This module exposes a wide set of utils methods and objects **_highly_** helpful for development.

For example: If you want to iterate for all the items in lol timeline events, **_it would be inefficient_** doing `await event.item.get()` for every event, because Pyot's stores makes sure that all data is **_safe_** from any type of mutation, so stores will automatically serialize and deserialize when accessing the object, which adds up CPU time overall. The solution would be a local `PtrCache` that saves references to the object without serializing it.

Another example: Pyot objects are _self filled_, therefore having them in lists will start filling the object in that list, allocating more memory over time, with a `FrozenGenerator` it will isolate the objects from the list by returning a copy on the iteration process.

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
