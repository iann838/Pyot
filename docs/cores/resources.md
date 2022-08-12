# Resources

{% hint style='info' %}
This page is of importance if your project is multithreaded, if you are not sure if your project is multithreaded, Pyot will automatically detect such environment and sends a warning. **You may choose to ignore this page if**:
- Your project runs single threaded or;
- Your project runs smoothly without implementing these concepts or;
- You choose to ignore all resource warnings and errors since they do not affect the main functionality of your prorject. 
{% endhint %}

Pyot acquires resources internally on-demand, on a traditional single threaded program, these resources remains mostly constant throughout the its runtime, and released automatically after the program exits.

However not all projects can be single threaded (usually unavoidable and required by other frameworks such as Django, Flask, DramatiQ, Celery, etc.), on a multithreaded environment, there is an event loop for each running thread, and these threads will be rotating and so the event loops, this causes two main issues for Pyot:

- Pyot must acquire new resources every time a new event loop attempts to use them, because most asyncio libraries and frameworks that Pyot is depending on are not designed to work in multithreaded environments (objects are bound to a specific event loop, limitations by python asyncio `Future`s and `Task`s).
- Pyot have no way to know when to release the unused resources because if they are released before the workflow is done, it will cause issue to the workflow, if they are released after the event loop is closed, the releasing functions cannot run because most of them requires to run on the same event loop before closing, and there is no 'magical' way of knowing the exact time of "right before event loop close".

For these reasons if you decide to use Pyot in a multithreaded environment, you will be responsible in telling Pyot "when" should it acquire and release resources in an event loop. Similar to other libraries using `async with` for management.

Alternatively, you can choose to simply ignore all warnings and errors, as they _likely won't_ prevent the code from running, Pyot will automatically check if there are resources in closed event loops and forcefully kill them to prevent memory leaks, this is of course not good pratice nor a graceful way of handling resources.

## Interfaces

Module: `pyot.core.resources`

### _class_ `ResourceManager`

Ensures acquisition and releasing of resources used by Pyot. Used as async context manager or as async function decorator.

Definitions:
* `__init__` -> `None`
    * `exist_ok`: `bool = False`
        > If another resource manager is currently active in the event loop, skip this context, avoid using this flag unless unavoidable.
* `__aenter__` -> `Self`
    > Acquire resources bound to instantiated event loop.
* `__aexit__` -> `None`
    > Release resources bound to instantiated event loop.

Properties:
* `loop` -> `asyncio.AbstractEventLoop`
* `exist_ok` -> `bool`

Methods: 
* _classmethod_ `as_decorator` -> `F~AsyncCallable`
    - `func`: `F~AsyncCallable`
    > Return a decorator that can be used for decorating async functions instead of using as context manager.
* _asyncmethod_ `acquire` -> `Self`
    > Explicit equivalent of `__aenter__`.
* _asyncmethod_ `release` -> `None`
    > Explicit equivalent of `__aexit__`.

### _alias_ `resource_manager` ~ `ResourceManager`

### _global_ `resource_managed_loops`: `Set[asyncio.AbstractEventLoop]`

Set of event loops with active resource managers.

### _class_ `ResourceTemplate`

Template for acquiring resources bound to event loops.
The submitted functions **must not implement locks**, it may cause deadlocks
because the acquisition and releasing process are also behind a lock.

Extends:

* `Generic[R]`

Definitions:

* `__init__` -> `None`
    * `acquire_func`: `Callable[[], Union[R, Awaitable[R]]]`
        > Function for acquiring the resource, the return value will be awaited if it is a coroutine.
    * `release_func`: `Callable[[R], Any] = ...`
        > Function for releasing the resource, the return value will be awaited if it is a coroutine. Optional.

Properties:

* `acquire_func`: `Callable[[], Union[R, Awaitable[R]]]`
* `release_func`: `Callable[[R], Any] = ...`

Methods:

* _asyncmethod_ `acquire` -> `Self`
    * `loop`: `asyncio.AbstractEventLoop = ...`
    > Acquire resource using `acquire_func` bound to the event loop, default current event loop if not provided.
* _asyncmethod_ `release` -> `None`
    * `loop`: `asyncio.AbstractEventLoop = ...`
    > Release resource using `release_func` bound to the event loop, default current event loop if not provided.
* _asyncmethod_ `purge` -> `None`
    > Purge acquired resources for all closed loops. Ungraceful release.

### _global_ `resource_templates`: `List["ResourceTemplate"]`

List of all instantiated resource templates by Pyot.


## Example

This example only serves for reference purpose only, there is zero reason to involve threads when the framework itself is async. Here theoretically `average_match_duration_millis` will run in threads on its own event loop, a `resource_manager` is used to properly acquire and release the resources (think of it as another `async with aiohttp.ClientSession()` but a much more complex one).

```python
from concurrent.futures import ThreadPoolExecutor
from typing import List
import statistics

from pyot.core.resources import resource_manager
from pyot.core.queue import Queue
from pyot.models import lol
from pyot.utils.sync import async_to_sync


@async_to_sync
async def average_match_duration_millis(summoner_name: str):
    # This function runs in a different thread and event loop
    async with resource_manager(), Queue() as queue:
        # At this point, resources are acquired for this event loop
        summoner = await lol.Summoner(name=summoner_name).get()
        history = await summoner.match_history.get()
        for match in history.matches[:5]:
            await queue.put(match.get())
        first_5_matches: List[lol.Match] = await queue.join()
    # At this point, resources are released for this event loop
    return statistics.mean([match.info.duration_millis for match in first_5_matches] or [0])

summoner_names = [...]
futures = []
with ThreadPoolExecutor() as executor:
    for summoner_name in summoner_names:
        futures.append(executor.submit(average_match_duration_millis, summoner_name))
    for future in futures:
        future.result()
```

There is a decorator version of resource manager, by decorating an async function instead of using as context manager, it will acquire resources before the function gets called and release them after the function is called. This may be more elegant for decorating functions like Django Views, DramatiQ or Celery tasks, etc.

```python
@async_to_sync
@resource_manager.as_decorator
async def average_match_duration_millis(summoner_name: str):
    # Before entering scope, resources are acquired for this event loop
    async Queue() as queue:
        summoner = await lol.Summoner(name=summoner_name).get()
        history = await summoner.match_history.get()
        for match in history.matches[:5]:
            await queue.put(match.get())
        first_5_matches: List[lol.Match] = await queue.join()
    return statistics.mean([match.info.duration_millis for match in first_5_matches] or [0])
    # After exiting scope, resources are released for this event loop
```
