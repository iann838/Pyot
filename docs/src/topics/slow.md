# Pyot slowing down on serialization

::: tip IMPORTANT FACT
Serialization of dicts to python objects (instantiation) will always add to processing time. In python, instantiation is relatively slow. This is a Python bottleneck, not a framework level bottleneck. The straight out solution is to write C code that can be imported to Python, but that is not something the maintainer is good at.
:::

The ***explanation and solution is given** using the `lol.MatchTimeline` or `lol.Timeline` objects from the lol model.

`MatchEventData` are usually **_large in numbers (hundreds per timeline)_**, Pyot **_can be slow_** when serializing these objects and creating the actual object (called instantiation). If you are bothered by performance issues, **_the recommended solution_** would be to access it as a dict to avoid the instantiation and serialization:

```python{2}
    # ...
    for event in timeline["events"]:
        # Do stuff with the event (as dictionary). Tested 5x faster.
```
The **_dict keys and values_** are the same as returned by the Riot API.

Another cause of slowness on `MatchTimeline`/ `Timeline` might be caused by data integrity protection of Pyot stores. Stores makes sure that all data is **_safe_** from any mutation, so stores will serialize and deserialize when accessing the object, which adds up significant amount of CPU time.

The solution is a local `PtrCache` cache from the utils module. Do not mutate objects saved on `PtrCache`, the cached object is **_not protected_**.

```python{8}
from pyot.utils import PtrCache
from pyot.models import lol

async def somefunc():
    cache = PtrCache()
    # ...
    for event in participant.timeline["events"]:
        item = await lol.Item(id=event['itemId'].get(ptr_cache=cache)) # intercepts the cache
```

**However this can still be improved**, you can avoid the instantiation of `lol.Item` completely by loading all the items at once or creating a function that delays the instantiation. This is 2 times faster than above implementation.

```python{8,12}
from pyot.utils import PtrCache
from pyot.models import lol

async def somefunc():
    item_cache = PtrCache()
    # ...
    for event in participant.timeline["events"]:
        item = item_cache.aget(event['itemId'], get_item(event['itemId']))

async def get_item(itemid):
    # Delays instantiation of lol.Item to only when needed
    return await lol.Item(id=event[itemid]).get()
```

**To improve it even further**, you can avoid the coroutine instantiation aswell, prefill the cache with all the items and set the expiration of the cache to forever so it never expires. This is 3 times faster than above implementation.

```python{6-8,11}
from pyot.utils import PtrCache
from pyot.models import lol

async def somefunc():
    item_cache = PtrCache(-1)
    items = lol.Items().get()
    for item in items:
        item_cache.set(item.id, item)
    # ...
    for event in participant.timeline["events"]:
        item = item_cache.get(event['itemId'])
```

It is best practice to have a different cache for different types of objects, so keys can be easily made unique.
