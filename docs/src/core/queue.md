# Queue

This is an object that executes coroutines in a queue/workers basic. Unlike Gatherer, this object creates true workers on the same thread, exposing the instance as a context manager that can be passed freely to coroutines, mostly for accessing the sid of the queue which is created similarly to Gatherer.

::: warning
This object is only accessible as a context manager with the `async with` syntax for safeguarding session closing and workers joining.
:::

## Pyot Queue API
A managed Queue on top of asyncio.Queue. This Queue is only usable as a context manager.

Unlike Gatherer, Queue has real workers that act like consumers.
A session is created and accessible on a 'sid' attribute. The maxsize will default to workers * 2.
Normally the queue object will be passed down to coroutines to give access to session id or queue methods. 

```python{1}
from pyot.core import Queue

async with Queue() as quque:
    # DO STUFF
```

> ### `__init__(workers: int = 25, maxsize: int = None, log_level: int = 10)`
> - `workers` <Badge text="param" type="warning" vertical="middle"/> -> `int`: Maximum number of workers to spawn for the queue. Increasing the number of workers may increase or decrease performance. Defaults to 25.
> - `log_level` <Badge text="param" type="warning" vertical="middle"/> -> `bool`: Set the log level for the Gatherer (does not affect pipeline logs). Defaults to 10 (DEBUG level).
> - `maxsize` <Badge text="param" type="warning" vertical="middle"/> -> `int`: Max size of the queue. Defaults to `workers * 2`.

> ### `put(coro: Coroutine, delay: float = 0)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
>Put a coroutine object to the queue. If the queue is full, it will wait for availability. A delay may be provided if desired for execution balancing.
> - `coro` <Badge text="param" type="warning" vertical="middle"/> -> `Coroutine`: The coroutine to put on the queue.
> - `delay` <Badge text="param" type="warning" vertical="middle"/> -> `float`: The amount of delay in seconds before putting the coroutine into the queue. Defaults to 0.

> ### `join()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>:
>Block until all items in the queue have been gotten and processed. Empty the collected responses and returns them. NoneType and Exceptions are not collected, thus order of the responses may not correspond the put order.

> ### `sid` <Badge text="property" type="error" vertical="middle"/>
> Property where the session id is stored, can be used to pass down to the Core objects `get()` to reuse a session.

> ### `responses` <Badge text="property" type="error" vertical="middle"/>
> Property where all the responses are saved, unlike Gatherer, this property **_is not safe to access_** as it may have inconsistency.

:::tip
You can use the same queue to `join()` as many time as you want, this creates a nice way to do everything in a single Queue. For example, get ChallengerLeague -> get all Summoners in the entries -> pull match history of all the Summoners.

It's best practice to pass the `sid` to the Core objects so that it can reuse a session, since creating a new session (created when no `sid` is provided) will cause some overhead.
:::

## Example Usage
```python{11,14,22,25,26}
from typing import List
from pyot.models import lol
from pyot.core import Queue
from pyot.utils import FrozenGenerator, shuffle_list

async def get_puuid(queue: Queue, summoner: lol.Summoner):
    summoner = await summoner.get(sid=queue.sid)
    return summoner.puuid

async def pull_puuids():
    async with Queue() as queue: # type: Queue
        await queue.put(lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="na1").get(sid=queue.sid))
        await queue.put(lol.MasterLeague(queue="RANKED_SOLO_5x5", platform="na1").get(sid=queue.sid))
        leagues = await queue.join() # type: List[lol.ChallengerLeague]

        summoners = []
        for league in leagues:
            for entry in league.entries:
                summoners.append(entry.summoner)
        # Shuffles the list by platform to balance rate limits by region 
        # Also freezes the list to prevent mutation that causes memory leak
        summoners = FrozenGenerator(shuffle_list(summoners, "platform"))

        for summoner in summoners:
            await queue.put(get_puuid(queue, summoner))
        print(await queue.join())
```
:::danger MEMORY AWARENESS
The coroutine passed to the queue. Try your best to not return anything or return small objects, because `Queue` will save those returning values for the `join()`, meaning that memory can start to increase over time. Try to design the coroutines to consume the object instead.

Assuming we want to gather 30k matches, take the following examples in term of memory usage
* ***BAD***
```python
def get_matches():
    matches = list_with_30k_match_timelines # <-- Suppose

    async with Queue() as queue: # type: Queue
        for match in matches:
            await queue.put(match.get(sid=queue.sid))
```
* ***GOOD***
```python
def get_matches():
    matches = list_with_30k_match_timelines # <-- Suppose
    matches = FrozenGenerator(matches) # Freezes the list to prevent mutation

    async with Queue() as queue: # type: Queue
        for match in matches:
            await queue.put(consume_match(queue, match))

def consume_match(queue, match):
    match.get(sid=queue.sid) # pass the session to reuse
    # ...
    # Consume your match (e.g. get specific stat, mutate a dictionary, save to db, etc.) ...
    # ...
    return None
    # OR no return at all (When no return is stated, defaults to return None)
```
:::
:::tip DETAILS
* `FrozenGenerator` was used to isolate the Summoners objects so that it doesn't pass by reference; therefore, not mutating the original list and prevent possible memory leak.
* `shuffle_list` was used to shuffle the list by `"platform"` to take advantage of crossing the waiting time on the rate limits for the different regions.
* A good use of inline type hinting can help you with IDE autocompletion. Note: You might not use this if responses contain more than 1 Pyot Core object type.
:::
