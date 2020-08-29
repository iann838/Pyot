# Django Integration

Djot is an installable app that will integrate Pyot to your Django application by taking care of the Pyot Settings.
This little app is installed together with Pyot.

## Setup

Create a file (preferably named `djot.py`) under any of the Django modules (either under an app folder or project folder):

This example will take `test` as the project directory, so create a `djot.py` file inside it and add up the needed Pyot Settings.
:::tip INFO
The below example settings is AN EXAMPLE, you can customize the Settings for your needs. Don't forget to activate the settings.
:::
```python{1,3,9,62}
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
            "EXPIRATIONS": {
                "summoner_v4_by_name": 0,
                "league_v4_challenger_league": td(minutes=10),
            }
        },
        {   
            # If you want to use Django Cache for the pipeline, read the Stores section
            "BACKEND": "pyot.stores.DjangoCache",
            "ALIAS": "pyot-redis",
            "EXPIRATIONS": {
                "summoner_v4_by_id": td(seconds=10),
                "*": 0
            }
        },
        {
            "BACKEND": "pyot.stores.MerakiCDN",
            "LOGS_ENABLED": True,
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.CDragon",
            "LOGS_ENABLED": True,
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "KEY": os.environ["RIOT_API_KEY"],
            "LIMITING_SHARE": 1,
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3,3])
            }
        }
    ]
).activate()
```
Then in your projects `settings.py` file, add `djot` to the `INSTALLED_APPS`.

```python{8}
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
```python{2}
PYOT_SETTINGS = [
    'test.djot'
]
```
:::tip INFO
You can define multiple settings in different files if you want to keep 1 setting per app (supposing you have 1 app per game model)
:::

## Example Usage
:::tip INFO
Djot is only for taking care of the Settings, you will keep using Pyot and/or Syot in your code.
:::

Views:
```python{4}
import pyot

async def mainview(request):
    summoner = await pyot.lol.Summoner(name="Morimorph", platform="NA1").get()
    context = {"level": summoner.level}
    return render(request, "yourview.html", context)
```
::: tip INFO
You can use `pyot.run()` to run pyot objects if your view is synchronous, or even use Syot instead.
GOOD TO KNOW: Syot and Pyot shares the same pipeline for each model.
:::

```python{4}
import pyot

def mainview(request):
    summoner = pyot.run(pyot.lol.Summoner(name="Morimorph", platform="NA1").get())
    context = {"level": summoner.level}
    return render(request, "yourview.html", context)
```

```python{4}
import syot

def mainview(request):
    summoner = syot.lol.Summoner(name="Morimorph", platform="NA1").get()
    context = {"level": summoner.level}
    return render(request, "yourview.html", context)
```