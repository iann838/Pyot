# Queue

This is an object that executes coroutines in a queue/workers basic. Unlike Gatherer, this object creates true workers on the same thread, exposing the instance as a context manager that can be passed freely to coroutines, mostly for accessing the sid of the queue which is created similarly to Gatherer.

::: warning
This object is only accessible as a context manager with the `async with` syntax for safeguarding session closing and workers joining.
:::

## Pyot Queue API
A managed Queue on top of asyncio.Queue. This Queue is only usable as a context manager.

Unlike Gatherer, Queue has real workers that acts like consumers.
A session is created and accessible on 'sid' attribute, the maxsize will default to workers * 2.
Normally the queue object will be passed down to coroutines to give access to session id or queue methods. 

```python
from pyot.core import Queue

async with Queue() as quque:
    # DO STUFF
```

> ### `__init__(workers: int = 25, maxsize: int = None, log_level: int = 20)`
> - `workers` <Badge text="param" type="warning" vertical="middle"/> -> `int`: Maximum number of workers to spawn for the queue. Increasing the number of workers may increase or decrease performance. Defaults to 25.
> - `log_level` <Badge text="param" type="warning" vertical="middle"/> -> `bool`: Set the log level for the Gatherer (does not affect pipeline logs). Defaults to 20 (INFO level).
> - `maxsize` <Badge text="param" type="warning" vertical="middle"/> -> `int`: Max size of the queue. Defaults to `workers * 2`.

> ### `put(coro: Coroutine, delay: float = 0)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
>Put a coroutine object to the queue, if the queue is full, wait for availability. A delay may be provided if desired for execution balancing.
> - `coro` <Badge text="param" type="warning" vertical="middle"/> -> `Coroutine`: The coroutine to put on the queue.
> - `delay` <Badge text="param" type="warning" vertical="middle"/> -> `float`: The amount of delay in seconds before putting the coroutine into the queue. Defaults to 0.

> ### `join()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>:
>Block until all items in the queue have been gotten and processed. Empty the collected responses and returns them. NoneType and Exceptions are not collected, order of the responses might not correspond the put order.

> ### `responses` <Badge text="property" type="error" vertical="middle"/>
> Property where all the responses are saved, unlike Gatherer, this property **_is not safe to access_** as it may have inconsistenty.

:::tip
You can use the same queue to `join()` as many time as you want, this creates a nice way to do everything in a single Queue, For example: get ChallengerLeague -> all Summoner in the entries -> pull all MatchHistory of the gotten Summoners.
:::

## Example Usage
```python{11,12,13,14,23,24}
from typing import List
from pyot.models import lol
from pyot.core import Queue
from pyot.utils import CloneGenerator, shuffle_list, loop_run

async def get_puuid(queue: Queue, summoner: lol.Summoner):
    summoner = await summoner.get(sid=queue.sid)
    return summoner.puuid

async def pull_puuids():
    async with Queue(log_level=30) as queue: # type: Queue
        await queue.put(lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="na1").get(sid=queue.sid))
        await queue.put(lol.MasterLeague(queue="RANKED_SOLO_5x5", platform="na1").get(sid=queue.sid))
        leagues = await queue.join() # type: List[lol.ChallengerLeague]
        
        _summoners = []
        for league in leagues:
            for entry in league.entries:
                _summoners.append(entry.summoner)
        summoners = CloneGenerator(shuffle_list(_summoners, "platform"))

        for summoner in summoners:
            await queue.put(get_puuid(queue, summoner))
        print(await queue.join())

loop_run(pull_puuids)
```
:::tip DETAILS
* `CloneGenerator` was used to isolate the summoners objects so it doesn't pass by reference and therefore not filling up the original list and prevent possible memory leak.
* `shuffle_list` was used to shuffle the list by `"platform"` to take advantage of crossing the waiting time on the rate limiters for the different regions.
* A good use of inline type hinting can help you with IDE autocompletion. Note: You might not use this if responses contains more than 1 type of Pyot Core objects.
:::
