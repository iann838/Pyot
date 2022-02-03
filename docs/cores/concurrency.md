# Concurrency

One of the benefits of asynchronous programming is that it allows concurrency. In Python, multiple tasks can start, run and complete in overlapping time periods.

Pyot provides a production rated queue manager to achieve high magnitude of concurrency in a stable manner.

## Queue

Module: `pyot.core.queue`

Worker queue for scheduling coroutines concurrently.

{% hint style='info' %}
This object is only accessible as a context manager with the `async with` syntax for safeguarding session closing and workers joining.
{% endhint %}

### _class_ Queue

Definitions:
* `__init__` -> `None`
  * `workers`: `int = 25`
    > Maximum number of workers to spawn for the queue. Increasing the number of workers may increase or decrease performance. Defaults to 25.
  * `maxsize`: `int = None`
    > Max size of the queue. Defaults to `workers * 2`.
  * `log_level`: `int = 0`
    > Log level for the que (does not affect pipeline logs). Defaults to 0 (NOLOG level).
  * `exception_handler`: `Callable[[Exception], Any] = LOGGER.warning`
    > Handler for raised exceptions in workers, defaults to logging a message with level 30 (WARNING).

Attributes:

* `queue`: `asyncio.Queue`
* `workers_num`: `int`
* `maxsize`: `int`
* `responses`: `Dict`
* `counter`: `int`
* `workers`: `List`
* `exception_handler`: `Callable[[Exception], Any]`

Methods:

* _async_ `put` -> `None`
  * `coro`: `Coroutine`
    > Coroutine to put on the queue.
  * `delay`: `float`
    > Amount of delay in seconds before putting the coroutine into the queue. Defaults to 0 (No delay).
  > Put a coroutine object to the queue. If the queue is full, wait for availability. A delay may be provided if desired for load balancing.

* _async_ `join` -> `List[T]`
  * `class_of_t`: `Optional[Type[T]]`
    > Optional, Generic type for typing the return content of this method (e.g `await queue.join(int)` will return a list typed as `List[int]`).
  > Block until all items in the queue have been received and executed. Clears the previously collected items if exists. NoneType and Exceptions are not collected, order of items is maintained but not guaranteed.

{% hint style='info' %}
You can use the same queue to `join()` as many time as you want, it will clear previous collected responses, this creates a nice way to do everything in a single Queue. Method `join()` will be automatically called before exiting the `async with` block, it is not needed to call explicitly unless the content of it is needed.
{% endhint %}

### Example Usage
```python
from pyot.models import lol
from pyot.core.queue import Queue

async def get_puuid(summoner: lol.Summoner):
    summoner = await summoner.get()
    return summoner.puuid

async def pull_puuids():
    async with Queue() as queue:
        await queue.put(lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="na1").get())
        await queue.put(lol.MasterLeague(queue="RANKED_SOLO_5x5", platform="na1").get())
        leagues = await queue.join(lol.ChallengerLeague) # Param is optional, used for typing only

        summoners = []
        for league in leagues:
            for entry in league.entries:
                summoners.append(entry.summoner)

        for summoner in summoners:
            await queue.put(get_puuid(summoner))
        return await queue.join(str)
```

{% hint style='danger' %}
Try not to return anything or return small objects in coroutines passed to the queue, because `Queue` will save those return values for the `join()`, meaning that memory can start to increase over time. Design async functions to consume data instead.

Objects instantiated outside of async functions holds reference in an upper scope, these objects can become a source of memory leaks if the data it holds (or will hold after mutations executed by coroutines) is big enough. To counter this:
- Instantiate objects inside async functions (e.g. Pass the id and region of a match and instantiate inside the function instead of passing a `lol.Match` object), so it can be garbage collected when it goes out of scope and nothing else holds reference to it.
- If the objects are inside an iterable and is planned to be mutated and filled with more data (e.g. calling `.get()` on PyotCore objects), freeze the iterable with an utility container `pyot.utils.itertools.FrozenGenerator`, it creates exact copies of the objects when iterated, therefore dropping the outer scope reference, the original object will be left intact.
{% endhint %}

Assuming the need to collect 30k matches, this will lead to a high use of memory:
```python
# ... imports

async def get_matches():
    matches = list_with_30k_matches
    async with Queue() as queue:
        for match in matches:
            await queue.put(match.get())
```
Instead, consume the matches directly instead of collecting them. The list is frozen to prevent memory usage since the child function calls `.get()` on the match.
```python
# ... imports
from pyot.utils.itertools import frozen_generator

async def get_matches():
    matches = list_with_30k_matches
    matches = frozen_generator(matches) # Freezes the list to prevent mutation
    async with Queue() as queue:
        for match in matches:
            await queue.put(consume_match(match))

async def consume_match(match):
    match.get() # pass the session to reuse
    # ...
    # Consume your match (e.g. get specific stat, mutate a dictionary, save to db, etc.) ...
    # ...
    return None
    # OR no return (When no return is stated, returns None by default)
```
