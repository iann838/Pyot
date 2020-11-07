# Pyot
[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/paaksing/pyot/blob/master/LICENSE)

> ## About the documentation
> The documentation is separated into different pages at the top navbar.
> - **_Core_** section documents the core modules, objects and settings of Pyot.
> - **_Pipeline_** section documents the Low level API of Pyot's Pipeline objects.
> - **_Models_** section documents the objects APIs for each available model.
> - **_Stores_** section documents the available Stores configurable to the pipeline.
> - **_Limiters_** section documents the available Rate Limiters for the RiotAPI Store.
> - **_Utils_** section documents the available helper functions and objects of Pyot.
> - **_Developers_** section has contributing guidelines and wanted features.
>
> Portal: [Pyot Documentations](https://paaksing.github.io/Pyot/)

Pyot is a Python Framework for the Riot Games API, including League of Legends, Teamfight Tactics, Valorant and Legend of Runeterra (soon). It specializes at doing task in async environment to get the expected result faster than synchronous code. Pyot is highly inspired by [Cassiopeia](https://github.com/meraki-analytics/cassiopeia), you will notice that it has similar approach and structure.

> #### WARNING
> For all users that has Pyot version v1.1.3 or lower please update to v1.1.4 or higher which contains potential fixes to rate limiters. 

## Features

Read this entirely to get a better idea of what is Pyot possible at.

- **_AsyncIO Based_**: No more waiting forever, concurrent calls and jobs made faster, highly configurable settings and wide range of tools to speed you right now.
- **_Synchronous Compatible_**: An adapted version of Pyot that runs on synchronous environment, **Pyot will expose part of its API synchronously in its secondary module called Syot**.
- **_Django Support_**: Full support for Django Caches Framework and its new 3.1 async Views, just add `pyot` to the installed apps and point your setting modules on your `settings.py` file.
- **_Community Projects Integrated_**: Take a step to dump the late and poor updated DDragon, we going beta testing directly using Cdragon and Meraki, BangingHeads' DDragon replacement is also coming soon.
- **_Caches Integrated_**: A wide range of Caches Stores is available right out of the box, we currently have Omnistone(Runtime), RedisCache(RAM), DiskCache(Disk) and MongoDB(NoSQL).
- **_Multiple Models_**: Available models are League of Legends, Teamfight Tactics, Legends of Runeterra and Valorant.
- **_Autocompletion Included_**: Forget the standard dictionary keys, triple your code efficiency now with autocompletion enabled.
- **_Perfect Rate Limiter_**: Pyot Rate Limiter is production tested in all asynchronous, multithreaded and even multiprocessed environments, rate limiters for perfectionists.
- **_User Friendly Docs_**: Meet a friendly docs that "should" be easier to read and understand.

## Requirements

- A computer/laptop with electricity and internet connection.
- Know what is and how to code in Python.
- Ability to read the docs.
- Python version >= 3.7.
- Django version >= 3.0 if used.

## Installation

```python
pip install pyot
```

## Quick Start

Activate the Pyot Settings for the model before entering main program, or on the `__init__.py` of your working module.

```python
from pyot.core import Settings
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

Pyot Settings should be **_activated_** on your main module's `__init__.py` or before your script `main()` entry point.
```python
├─ foo
│  ├─ __init__.py  # <---- HERE MOSTLY
│  ├─ __main__.py  # <---- OR ANYWHERE BEFORE CALLING `main()`
│  └─ bar.py
# ...
```

> This pipeline settings is only specific to League of Legends Model, for example, TFT doesn't have support of the MerakiCDN.

Now in your main file or module.

```python
from pyot.models import lol
from pyot.utils import loop_run

async def main():
    summoner = await lol.Summoner(name="Morimorph", platform="NA1").get()
    print(summoner.level)

loop_run(main())
```

> There is an [issue](https://github.com/aio-libs/aiohttp/issues/4324) on aiohttp related to a `ProactorConnector` Error when used with `asyncio.run()` on Windows (it appears to be closed but more related issue surged because of this), `loop_run()` is the same as `asyncio.get_event_loop().run_until_complete()` imported from the utils module of pyot.

# Django

Plugging Pyot into Django is really easy.

> #### DEPRECATED
> Since v1.1.0: The module `djot` for Django has been removed, now `pyot` can be installed natively.

## Installation

Create a file (the example will use `pipelines.py`) under any of the Django modules (either under an app folder or project folder):

This example has `test` as the project directory and `pipelines.py` as the module. Inside the file add up the needed Pyot Settings. The below example settings is AN EXAMPLE, you can customize the Settings for your needs. Don't forget to activate the settings.

```python
#test/pipelines.py

from pyot.core import Settings
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
            "API_KEY": os.environ["RIOT_API_KEY"],
        }
    ]
).activate()
```
Then in your projects `settings.py` file, add `pyot` to the `INSTALLED_APPS`.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pyot',
]
```
In the same `settings.py` file, add the file path to a reserved variable for Pyot called `PYOT_SETTINGS`.
```python
# Supposing the pyot settings file is at: test/pipelines.py

PYOT_SETTINGS = [
    'test.pipelines'
]
```
You can define multiple settings in different files if you want to keep 1 setting per app (supposing you have 1 app per game model).

# Syot

Syot is a back ported version of Pyot to synchronous code (rarely a case not going async), this might be an option for those who don't want to go async or wants flexibility by using both async and sync code at the same time, which is in some case for Django views.

>You still need to activate the Settings for Syot to work.

>Syot and Pyot **_shares the same pipeline_** per each model so you can use both environment together without problem of any. They won't have any conflict unless you try to activate the same Settings twice both in Syot and Pyot.

Below documentation only applies to Syot.
The rest of the API please refer to Pyot documentation by replacing `pyot` with `syot` instead, awaitables needs to be executed with `loop_run()`.

## Similarities
1. All Pyot Object's methods that are not marked with "awaitable" are usable in Syot, that includes Pyot Object's `dict()`, `json()` and others not mentioned.
2. All the models API are available on Syot, with some minor changes listed below.

## Differences
1. Lose the advantage of cooperative tasks and high concurrency to speed up the calls.
2. The Pyot Pipeline Low Level API is not available in synchronous environment, you would need to do `loop_run()` for every single pipeline coroutine.
3. The Pyot Gatherer is also not supported here, because it is a feature only for asynchrounous environment.
4. Instead of `from pyot` do `from syot` to import the synchronous version of Pyot.
5. You no longer need to `await` the `get()` methods on the Objects, and `get()` is now "chainable", meaning you can chain attributes and other methods right after `get()`.

## Example Usage
Activate the settings before you script entry point or module `__init__.py`
```python
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
```python
from syot.models import lol

summoner = lol.Summoner(name="Morimorph", platform="NA1").get()
print(summoner.level)

#OR using method chains:
print(lol.Summoner(name="Morimorph", platform="NA1").get().level)
```

# Contributing

Contributions are welcome! If you have idea or opinions on how things can be improved, don’t hesitate to let us know by posting an issue on GitHub or @ing me on the Riot API Discord channel. And we always want to hear from our users, even (especially) if it’s just letting us know how you are using Pyot.
