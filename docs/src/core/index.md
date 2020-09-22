# Pyot
##### <Badge text="Staging" vertical="middle"/> [<Badge text="MIT Licensed" type="warning" vertical="middle"/>](https://github.com/paaksing/pyot/blob/master/LICENSE)

:::tip ABOUT THIS DOCUMENTATION
The documentation is separated into different pages at the top navbar.
- **_Core_** section documents the core modules, objects and settings of Pyot.
- **_Pipeline_** section documents the Low level API of Pyot's Pipeline objects.
- **_Models_** section documents the objects APIs for each available model.
- **_Stores_** section documents the available Stores configurable to the pipeline.
- **_Limiters_** section documents the available Rate Limiters for the RiotAPI Store.
- **_Utils_** section documents the available helper functions and objects of Pyot.
- **_Developers_** section has contributing guidelines and wanted features.
:::

Pyot is a Python Framework for the Riot Games API, including League of Legends, Teamfight Tactics, Valorant and Legend of Runeterra (soon). It specializes at doing task in async environment to get the expected result faster than synchronous code. Pyot is highly inspired by [Cassiopeia](https://github.com/meraki-analytics/cassiopeia), you will notice that it has similar approach and structure.

## Features

Read this entirely to get a better idea of what is Pyot possible at.

- **_AsyncIO Based_**: No more waiting forever, concurrent calls and jobs made faster, highly configurable settings and wide range of tools to speed you right now.
- **_Synchronous Compatible_**: An adapted version of Pyot that runs on synchronous environment, **Pyot will expose part of its API synchronously in its secondary module called [Syot](syot.html)** <Badge text="installed by default" vertical="middle"/>.
- **_Django Support_**: Full support for Django Caches Framework and its new 3.1 async Views, just add `pyot` to the installed apps and point your setting modules on your `settings.py` file. [More details](django.html).
- **_Community Projects Integrated_**: Take a step to dump the late and poor updated DDragon, we going beta testing directly using Cdragon and Meraki, BangingHeads' DDragon replacement is also coming soon.
- **_Caches Integrated_**: A wide range of Caches Stores is available right out of the box, we currently have Omnistone(Python), RedisCache(RAM), DiskCache(File) and soontm an SQL Cache.
- **_Multiple Models_**: Available models are League of Legends, Teamfight Tactics and Valorant, holding onto Legend of Runeterra.
- **_Autocompletion Included_**: Forget the standard dictionary keys, triple your code efficiency now with autocompletion enabled.
- **_Perfect Rate Limiter_**: Pyot Rate Limiter is production tested in all asynchronous, multithreaded and even multiprocessed environments, rate limiters for perfectionists.
- **_User Friendly Docs_**: Meet a friendly docs that "should" be better to read and understand.

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

:::tip
For Django Setup, please refer to Django section on the sidebar.
:::

Activate the Pyot Settings for the model before entering main program, or on the `__init__.py` of your working module.

```python{15,18}
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
:::tip NOTE
This pipeline settings is only specific to League of Legends Model, for example, TFT doesn't have support of the MerakiCDN.
:::

Now in your main file or module.

```python{5}
from pyot.models import lol
from pyot.utils import loop_run

async def main():
    summoner = await lol.Summoner(name="Morimorph", platform="NA1").get()
    print(summoner.level)

loop_run(main())
```
::: tip INFO
There is an [issue](https://github.com/aio-libs/aiohttp/issues/4324) on aiohttp related to a `ProactorConnector` Error when used with `asyncio.run()` on Windows (it appears to be closed but more related issue surged because of this), `loop_run()` is the same as `asyncio.get_event_loop().run_until_complete()` imported from the utils module of pyot.
:::

## Contributing

Contributions are welcome! If you have idea or opinions on how things can be improved, don’t hesitate to let us know by posting an issue on GitHub or @ing me on the Riot API Discord channel. And we always want to hear from our users, even (especially) if it’s just letting us know how you are using Pyot.
