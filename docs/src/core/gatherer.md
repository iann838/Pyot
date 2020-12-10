# Gatherer

This is an object to gather data by chunks, creates a session and store this session under each of the pipelines `sessions` dict with an `uuid4()` key to give the highest uniqueness possible, this session id is added to each of the objects in the `statements` provided. After finishing the execution of all the statements, it then proceed to delete the session from the pipeline. 

:::tip ABOUT
This manager is only recommended for working with small amount of Pyot Core Objects for short time bursts. If you need to execute custom tasks written by you or working with large amount of objects, you should go with [Queue](queue.html) instead.
:::

:::warning INFO
All of the `statements` provided needs to be an instance of the Pyot Core object and **_`get()` must NOT be appended to the instance, as `get()` is "unchainable" so Pyot Gatherer has no way of calling `get(sid=...)` again_**. It will raise a `RuntimeError` if this happens.

`query()` and other methods (that are not coroutines) that returns `self` **_are safe and can be appended to the `statement`_**.
Pyot Gatherer will automatically append `get()` to the instance after setting the session id.

Gatherer workers are NOT real workers, that is the size of the chunk to gather.
:::
:::danger MEMORY AWARENESS
Misusing the Gatherer might end up causing memory leaks, consider the following example:
```python{4}
matches = list_with_30k_match_timelines # <-- Suppose
async with Gatherer() as gatherer:
    gatherer.statements = matches
    await gatherer.gather() # <-- This will load aprox. 10 GB to memory
```
The why of this is because `matches` is a mutable object, so it will be passed to the gatherer by reference, it will endup filling up the 30k matches on that list, a workaround would be to load your matches in a loop scope so Python can garbage collect it, or better use the utils `FrozenGenerator` plus the other gathering tool `Queue`.
:::

## Pyot Gatherer API
This object creates a manager that speeds up the normal data gathering, statements and responses are all instantiated to this object and can be referenced back.
This object is imported at the core module of pyot.

```python{1}
from pyot.core import Gatherer

async with Gatherer() as gatherer:
    # DO STUFF
```
:::warning
This object is preferably used as a context manager because it will clean up the instance after the `with` statement freeing memory, although nothing stops you from doing `gatherer = pyot.Gatherer()`.
:::
> ### `__init__(workers: int = 25, log_level: int = 10, cancel_on_raise: bool = False)`
> Creates an instance of Gatherer with the respective params, these params are set when Pyot Settings was set if specified the `GATHERER` param, you can also override partial settings at runtime by passing the params on instance creation:
> - `workers` <Badge text="param" type="warning" vertical="middle"/> -> `int`: Maximum number of concurrent connections and tasks allowed for this Gatherer. Increasing the number of workers may increase or decrease performance. Defaults to 25.
> - `log_level` <Badge text="param" type="warning" vertical="middle"/> -> `bool`: Set the log level for the Gatherer (does not affect pipeline logs). Defaults to 10 (DEBUG level).
> - `cancel_on_raise` <Badge text="param" type="warning" vertical="middle"/> -> `bool`: Cancel all remaining tasks if one raises exception. Defaults to `False`.

> ### `statements` <Badge text="property" type="error" vertical="middle"/>
> Property where statements are stored for gathering, it starts as an empty list, it can be used by `append()`-ing Pyot Core instances or directly override the list with a prepared one.

> ### `gather()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Starts by appending the new created session and the awaitable `get()` to the Pyot Core instance, then starts the gather process, once finished closes the session and saves all responses to `responses` and return it.

> ### `responses` <Badge text="property" type="error" vertical="middle"/>
> Property where all the responses are saved, developers would want to assign this data to a variable before leaving the `async with` statement.
>::: TIP
>Since v1.1.0 `gather()` will return `responses` by default.
>:::

:::tip
You can use the same gatherer to `gather()` multiple list of statements by overriding it after saving the responses, this creates a nice way to do everything in a single Gatherer, For example: get ChallengerLeague -> all Summoner in the entries -> pull all MatchHistory of the gotten Summoners.
:::

## Example Usage
```python{8-10}
from pyot.models import lol
from pyot.core import Gatherer
from pyot.utils import loop_run
from typing import List

async def pull_leagues():
    league = await lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="NA1").get()
    async with Gatherer() as gatherer: # type: pyot.Gatherer
        gatherer.statements = [entry.summoner for entry in league.entries]
        responses = await gatherer.gather() # type: List[pyot.lol.Summoner]
    for r in responses:
        print(r.profile_icon_id)

loop_run(pull_leagues())
```
:::tip
A good use of inline type hinting can help you with IDE autocompletion. For example in line 9 I added the type hint of the expected response objects class via comments then on the next `for` loop, you don't lose IDE autocompletion. Note: You might not use this if responses contains more than 1 type of Pyot Core objects.
:::
