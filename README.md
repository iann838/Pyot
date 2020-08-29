# Pyot
[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/paaksing/pyot/blob/master/LICENSE)

> The documentation is separated into different pages at the top navbar.
> - **_Framework Cores_** section documents the core settings and features that Pyot uses.
> - **_Models API_** section documents the API objects for each model.
> - **_Pipeline Stores_** section documents of the official stores configurable to the pipeline.
>
> Portal: [Pyot Documentations](https://paaksing.github.io/Pyot/)

Pyot is a Python Framework for the Riot Games API, including League of Legends, Teamfight Tactics, Valorant and Legend of Runeterra (soon). It specializes at doing task in async environment to get the expected result faster than synchronous code. Pyot is highly inspired by [Cassiopeia](https://github.com/meraki-analytics/cassiopeia), you will notice that it has similar approach and structure.

## Features

- **_AsyncIO Support_**: No more waiting forever, concurrent calls and jobs made faster, highly configurable semaphores and clients sessions to your needs.
- **_Django Support_**: Full support for Django Caches Framework and its new 3.1 async Views, **the Pyot Framework activation will be handled by an installable app called [Djot](https://paaksing.github.io/Pyot/cores/djot.html)**.
- **_Synchronous Adaptation_**: There is a adapted version that runs on synchronous environment, **Pyot will expose part of its API synchronously in the extended module called [Syot](https://paaksing.github.io/Pyot/cores/syot.html)** .
- **_Community Projects Integrated_**: Take a step to dump the late and poor updated DDragon, we going beta testing directly using Cdragon and Meraki.
- **_Stores Integrated_**: A runtime Cache is provided to avoid repeated calls, possible SQL and Redis store coming. For Django you have the integrated Django Cache Store.
- **_Multiple Models_**: Available models are League of Legends, Teamfight Tactics and Valorant, holding onto Legend of Runeterra.
- **_Autocompletion Included_**: Forget the standard dictionary keys, triple your code efficiency now.
- **_Perfect Rate Limiter_**: Rate Limiter is tested in asynchronous and multithreaded environments.
- **_User Friendly Docs_**: Meet a friendly docs that "should" be better to read and understand

## Requirements

- A computer/laptop with electricity and internet connection.
- Know what is and how to code in Python
- Python version 3.7 +
- Django version 3.0 + if used

## Installation

```python
pip install pyot
```

## Quick Start

Activate the Pyot Settings for the model before entering main program, or on the `__init__.py` of your working module.

```python
import pyot
import os

pyot.Settings(
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
            "KEY": os.environ["RIOT_API_KEY"], # API KEY
        }
    ]
).activate() # <- DON'T FORGET TO ACTIVATE THE SETTINGS
```
Note: This pipeline settings is only specific to League of Legends Model, for example, TFT doesn't have support of the MerakiCDN.

Now in your main file or module.

```python
import pyot

async def main():
    summoner = await pyot.lol.Summoner(name="Morimorph", platform="NA1").get()
    print(summoner.level)

pyot.run(main())
```
Note: There is an [issue](https://github.com/aio-libs/aiohttp/issues/4324) on aiohttp related to a `ProactorConnector` Error when used with `asyncio.run()` (it appears to be closed but more related issue surged because of this), `pyot.run()` is the same as `asyncio.get_event_loop().run_until_complete()`, just shortened for you.

# Djot

Djot is an installable app that will integrate Pyot to your Django application by taking care of the Pyot Settings.
This little app is installed together with Pyot.

## Setup

Create a file (preferably named `djot.py`) under any of the Django modules (either under an app folder or project folder):

This example will take `test` as the project directory, so create a `djot.py` file inside it and add up the needed Pyot Settings.
The below example settings is AN EXAMPLE, you can customize the Settings for your needs. Don't forget to activate the settings.

```python
#test/djot.py

import pyot
import os
import aiohttp
from datetime import timedelta as td


pyot.Settings(
    MODEL = "LOL",
    GATHERER = {
        "LOGS_ENABLED": True,
        "SESSION_CLASS": aiohttp.ClientSession,
        "CANCEL_ON_RAISE": False,
    },
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN_US",
    PIPELINE = [
        {
            "BACKEND": "pyot.stores.Omnistone",
        },
        {   
            # If you want to use Django Cache for the pipeline, read the Stores section
            "BACKEND": "pyot.stores.DjangoCache",
            "ALIAS": "pyot-redis",
        },
        {
            "BACKEND": "pyot.stores.MerakiCDN",
        },
        {
            "BACKEND": "pyot.stores.CDragon",
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "KEY": os.environ["RIOT_API_KEY"],
        }
    ]
).activate()
```
Then in your projects `settings.py` file, add `djot` to the `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djot',
]
```

In the same `settings.py` file, add the file path to a reserved variable for Djot called `PYOT_SETTINGS`.

Supposing the pyot settings file is at: `test/djot.py`
```python
PYOT_SETTINGS = [
    'test.djot'
]
```
You can define multiple settings in different files if you want to keep 1 setting per app (supposing you have 1 app per game model)

# Syot

Syot is an adaptation of Pyot to synchronous code (although I don't see a reason of not going async), this might be an option for those who don't want to go async or want to be REALLY FLEXIBLE by using the 2 world at the same time, which is in some case for Django views.

Syot and Pyot **_shares the same pipeline_** per each model so you can use the 2 world together without problem of any. They won't have any conflict UNLESS UNLESS and UNLESS you try to activate the same Settings twice both in Syot and Pyot.

## Similarities
1. All Pyot Object's methods that are not marked with "awaitable" are usable in Syot, that includes Pyot Object's `dict()`, `json()` and others not mentioned.
2. All the models API are available on Syot, with some minor changes listed below.

## Differences
1. Lose the advantage of cooperative tasks that speeds 100x the calls in exchange of flexibility or a ... mOrE rEAdAblE COdE ?
2. The Pyot Pipeline Low Level API is not available in synchronous environment, you would need to do `pyot.run()` for every single pipeline coroutine.
3. The Pyot Gatherer is also not supported here, because it is a feature only for asynchrounous environment.
4. Instead of `import pyot` do `import syot` to import the synchronous version of Pyot.
5. You no longer need to `await` the `get()` methods on the Objects, and `get()` is now "chainable", meaning you can chain attributes and other methods right after `get()`.

## Example Usage
Activate the settings before you script entry point or module `__init__.py`
```python
import syot
import os

syot.Settings(
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
            "KEY": os.environ["RIOT_API_KEY"], # API KEY
        }
    ]
).activate() # <- DON'T FORGET TO ACTIVATE THE SETTINGS
```
Example of Syot code
```python
import syot

summoner = syot.lol.Summoner(name="Morimorph", platform="NA1").get()
print(summoner.level)

#OR using method chains:
print(syot.lol.Summoner(name="Morimorph", platform="NA1").get().level)
```