# Pyot
##### <Badge text="Beta Testing" vertical="middle"/> [<Badge text="MIT Licensed" type="warning" vertical="middle"/>](https://github.com/paaksing/pyot/blob/master/LICENSE)

:::tip ABOUT THIS DOCUMENTATION
The documentation is separated into different pages at the top navbar.
- **_Framework Cores_** section documents the core settings and features that Pyot uses.
- **_Models API_** section documents the API objects for each model.
- **_Pipeline Stores_** section documents of the official stores configurable to the pipeline.

For some reason this page keeps going back to top when scrolled to #Pyot, if this happens just scroll pass it to #Features.
:::

Pyot is a Python Framework for the Riot Games API, including League of Legends, Teamfight Tactics, Valorant and Legend of Runeterra (soon). It specializes at doing task in async environment to get the expected result faster than synchronous code. Pyot is highly inspired by [Cassiopeia](https://github.com/meraki-analytics/cassiopeia), you will notice that it has similar approach and structure.

## Features

- **_AsyncIO Support_**: No more waiting forever, concurrent calls and jobs made faster, highly configurable semaphores and clients sessions to your needs.
- **_Django Support_**: Full support for Django Caches Framework and its new 3.1 async Views, **the Pyot Framework activation will be handled by an installable app called [Djot](djot.html)** <Badge text="installed by default" vertical="middle"/>.
- **_Synchronous Adaptation_**: There is a adapted version that runs on synchronous environment, **Pyot will expose part of its API synchronously in the extended module called [Syot](syot.html)** <Badge text="installed by default" vertical="middle"/>.
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

:::tip
For Django Setup, please refer to Djot section on the sidebar.
:::

Activate the Pyot Settings for the model before entering main program, or on the `__init__.py` of your working module.

```python{15,18}
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
:::tip NOTE
This pipeline settings is only specific to League of Legends Model, for example, TFT doesn't have support of the MerakiCDN.
:::

Now in your main file or module.

```python{4}
import pyot

async def main():
    summoner = await pyot.lol.Summoner(name="Morimorph", platform="NA1").get()
    print(summoner.level)

pyot.run(main())
```
::: tip INFO
There is an [issue](https://github.com/aio-libs/aiohttp/issues/4324) on aiohttp related to a `ProactorConnector` Error when used with `asyncio.run()` (it appears to be closed but more related issue surged because of this), `pyot.run()` is the same as `asyncio.get_event_loop().run_until_complete()`, just shortened for you.
:::
