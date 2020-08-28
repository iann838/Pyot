# Gatherer

The existence of this object is because of aiohttp's Docs:

>Don’t create a session per request. Most likely you need a session per application which performs all requests altogether.
>
>More complex cases may require a session per site, e.g. one for Github and other one for Facebook APIs. Anyway making a ses>sion for every request is a very bad idea.
>
>A session contains a connection pool inside. Connection reusage and keep-alives (both are on by default) may speed up total performance.

Normally the Pyot Pipeline will create a brand new session per `get()` and this is a bad idea as aiohttp docs says. So when doing large gathering of data, instead of using `asyncio.gather()` you can use this "gatherer".

It will create a session and store this session under each of the pipelines `sessions` dict with an `uuid4()` key to give the highest uniqueness possible, this session id is added to each of the objects in the `statements` provided. After finishing the execution of all the statements, it then proceed to delete the session from the pipeline. 

:::warning
All of the `statements` provided needs to be an instance of the Pyot Core object and **_`get()` must NOT be appended to the instance, as `get()` is "unchainable" so Pyot Gatherer has no way of calling `set_session_id()` on a coroutine_**. It will raise a `RuntimeError` if this happens.
:::
:::tip INFO
`query()` and other methods (that are not coroutines) that returns `self` **_are safe and can be appended to the `statement`_**.
Pyot Gatherer will automatically append `get()` to the instance after setting the session id.
:::

## Pyot Settings Reference
The settings params and default values for the `GATHERER` argument in Pyot Settings. Detailed explanation of each param is below.
:::tip
Keys can be ALL CAPS to keep settings clean.
For more in depth explanation of these params please refer to the Pyot Gatherer API section below.
:::
```python
{
    "workers": 200,
    "logs_enabled": True,
    "session_class": aiohttp.ClientSession,
    "cancel_on_raise": False,
}
```

## Pyot Gatherer API
This object creates a manager that speeds up the normal data gathering, statements and responses are all instantiated to this object and can be referenced back.
This object is imported at Pyot's root level as `Gatherer`.
```python{1,4}
import pyot
async with pyot.Gatherer() as gatherer:
# OR
from pyot import Gatherer
async with Gatherer() as gatherer:
```
:::warning
This object is preferably used as a context manager because it will clean up the instance after the `with` statement freeing memory, although nothing stops you from doing `gatherer = pyot.Gatherer()`
:::
> ### `__init__(workers: int = 200, session_class: Any = aiohttp.ClientSession, logs_enabled: bool = True, cancel_on_raise: bool = False)`
> Creates an instance of Gatherer with the respective params, these params are set when Pyot Settings was set if specified the `GATHERER` param, you can also override partial settings at runtime by passing the params on instance creation:
> - `workers` <Badge text="param" type="warning" vertical="middle"/> -> `int`: Maximum number of worker tasks allowed for this Gatherer to run concurrently, this is then set as `asyncio.Semaphore` for the gathering. Defaults to 200
> - `session_class` <Badge text="param" type="warning" vertical="middle"/> -> `Any`: The session class to be used for creating the session and used for gathering. Defaults to `aiohttp.ClientSession`
> - `logs_enabled` <Badge text="param" type="warning" vertical="middle"/> -> `bool`: Enables logs for the Gatherer (has nothing to do with pipeline logs). Defaults to `True`.
> - `cancel_on_raise` <Badge text="param" type="warning" vertical="middle"/> -> `bool`: Cancel all remaining tasks if one raises exception. Defaults to `False`.

> ### `statements` <Badge text="property" type="error" vertical="middle"/>
> Property where statements are stored for gathering, it starts as an empty list, it can be used by `append()`-ing Pyot Core instances or directly override the list with a prepared one.

> ### `gather()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Starts by appending the new created session and the awaitable `get()` to the Pyot Core instance, then starts the gather process, once finished closes the session and saves all responses to `responses`

> ### `responses` <Badge text="property" type="error" vertical="middle"/>
> Property where all the responses are saved, developers would want to assign this data to a variable before leaving the `async with` statement.

## Example Usage
```python{6-9}
import pyot
from typing import List

async def pull_leagues():
    league = await pyot.lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="NA1").get()
    async with pyot.Gatherer() as gatherer: # type: pyot.Gatherer
        gatherer.statements = [entry.summoner for entry in league.entries[:62]]
        await gatherer.gather()
        responses = gatherer.responses # type: List[pyot.lol.Summoner]
    for r in responses:
        print(r.profile_icon_id)

pyot.run(pull_leagues())
```
:::tip
A good use of inline type hinting can help you with IDE autocompletion. For example in line 9 I added the type hint of the expected response objects class via comments then on the next `for` loop, you don't lose IDE autocompletion. Note: You might not use this if responses contains more than 1 type of Pyot Core objects.
:::
