# Pyot
[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/paaksing/pyot/blob/master/LICENSE)

Pyot is a Python Framework for the Riot Games API, including League of Legends, Teamfight Tactics, Valorant and Legend of Runeterra (soon).

## Requirements

- A computer/laptop with electricity and internet connection.
- Know what is and how to code in Python
- Python version 3.7 +
- Django version 3.0 + if used

## Installation

```python
pip install pyot
```

## Features

- **_AsyncIO Support_**: No more waiting forever, concurrent calls and jobs made faster, highly configurable semaphores and clients.
- **_Django Support_**: Full support for Django Caches Framework and its new 3.1 async Views, extended as Djot (installed).
- **_Community Projects Integrated_**: Take a step to dump DDragon, I got Cdragon and Meraki on your back.
- **_Stores Integrated_**: A runtime Cache is provided to avoid repeated calls, possible SQL and Redis store coming.
- **_Multiple Models_**: Available models are League of Legends, Teamfight Tactics and Valorant, holding onto Legend of Runeterra.
- **_Autocompletion Included_**: Forget the standard dictionary keys, triple your code efficiency now.
- **_Synchronous Adaption_**: There is a adapted version that runs on synchronous environment called Syot (installed).
- **_Perfect Rate Limiter_**: Rate Limiter is tested in asynchronous and multithreaded environments.
- **_User Friendly Docs_**: Meet a friendly docs that "should" be better to read and understand

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
Note: There is an open issue on aiohttp related to a `ProactorConnector` Error when used with asyncio.run(), `pyot.run()` is the same as `asyncio.get_event_loop().run_until_complete()`, just shortened for you.

If you're using Django, then you can do the following.
Note: You can use `pyot.run()` to run pyot objects if your view is synchronous

```python
import pyot

async def mainview(request):
    summoner = await pyot.lol.Summoner(name="Morimorph", platform="NA1").get()
    context = {"level": summoner.level}
    return render(request, "yourview.html", context)
```
