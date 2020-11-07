# Syot

Syot is a back ported version of Pyot to synchronous code (rarely a case not going async), this might be an option for those who don't want to go async or wants flexibility by using both async and sync code at the same time, which is in some case for Django views.

:::tip INFO
You still need to activate the Settings for Syot to work.
:::

:::warning
Syot and Pyot **_shares the same pipeline_** per each model so you can use both environment together without problem of any. They won't have any conflict unless you try to activate the same Settings twice both in Syot and Pyot.
:::

Below documentation only applies to Syot.
The rest of the API please refer to Pyot documentation by replacing `pyot` with `syot` instead, awaitables needs to be executed with `loop_run()`.

## Similarities
1. All Pyot Object's methods that are not marked with <Badge text="awaitable" type="error" vertical="middle"/> are usable in Syot, that includes Pyot Object's `dict()`, `json()` and others not mentioned.
2. All the models API are available on Syot, with some minor changes listed below.

## Differences
1. Lose the advantage of cooperative tasks and high concurrency to speed up the calls.
2. The Pyot Pipeline Low Level API is not available in synchronous environment, you would need to do `loop_run()` for every single pipeline coroutine.
3. The Pyot Gatherer is also not supported here, because it is a feature only for asynchrounous environment.
4. Instead of `from pyot` do `from syot` to import the synchronous version of Pyot.
5. You no longer need to `await` the `get()` methods on the Objects, and `get()` is now "chainable", meaning you can chain attributes and other methods right after `get()`.

## Example Usage
Activate the settings before you script entry point or module `__init__.py`
```python{1,4,15,18}
from syot.core import Settings
import os

Settings(
    MODEL = "LOL",
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN_US",
    PIPELINE = [
        {"BACKEND": "pyot.stores.Omnistone"},
        {"BACKEND": "pyot.stores.MerakiCDN"},
        {"BACKEND": "pyot.stores.CDragon"},
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "API_KEY": os.environ["RIOT_API_KEY"], # API KEY
        }
    ]
).activate() # <- DON'T FORGET TO ACTIVATE THE SETTINGS
```
Example of Syot code
```python{1,3,7}
from syot.models import lol

summoner = lol.Summoner(name="Morimorph", platform="NA1").get()
print(summoner.level)

#OR using method chains:
print(lol.Summoner(name="Morimorph", platform="NA1").get().level)
```