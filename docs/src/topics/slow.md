# How to optimize Pyot CPU time

:::tip UPDATE
Since Pyot 3, serialization is 3 ~ 5 times faster than Pyot 2. But this topic still remains useful and applicable.
:::

When the response is going to the Python level (Objects) it needs to be serialized and extra CPU time is used to do so.
The ***optimization sample below is given** using the `lol.Match` or `lol.Timeline` objects from the lol model.

`MatchEventData` are usually **_large in numbers (hundreds per timeline)_**, Pyot can be **_slower_** when serializing these objects. If you are bothered by performance issues, **_the recommended solution_** would be to access it as a dict to avoid the instantiation and serialization:

```python{2}
    # ...
    for event in timeline["events"]:
        item_id = event["itemId"]
        # Do stuff with the event (as dictionary). Tested 5x faster.
```
The **_dict keys and values_** are the same as returned by the Riot API.

Slow CPU time might be caused by data integrity protection of Pyot stores. Stores makes sure that all data is **safe** from any mutation, so stores will serialize and deserialize when accessing the object, which adds up significant amount of CPU time.

The solution is a local `PtrCache` cache from the utils module. Do not mutate objects saved on `PtrCache`, the cached object is **not protected**. There is multiple level of optimization you can do with this cache, breaking it down:

### Level 1 - Basic usage

```python{8,12}
from pyot.utils import PtrCache
from pyot.models import lol

async def somefunc():
    item_cache = PtrCache()
    # ...
    for event in participant.timeline["events"]:
        item = item_cache.aget(event['itemId'], lol.Item(id=event[itemid]).get())
```

### Level 2 - Lazy evaluation

Delay the coroutine instantiation or any object instantiation that comes before it, the PtrCache object provides a `lazy` param (since v3.0.0) to delay the instantiation.

```python{8,12}
from pyot.utils import PtrCache
from pyot.models import lol

async def somefunc():
    item_cache = PtrCache()
    # ...
    for event in participant.timeline["events"]:
        item = item_cache.aget(event['itemId'], lambda: lol.Item(id=event[itemid]).get(), lazy=True)
```

### Level 3 - Precaching

You can precache all expected data as never-expire at the beginning to avoid lambda evaluation and multiple handler function running at once.

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
