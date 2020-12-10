# Django

Integrating Pyot into Django is easy.

## Installation

Create a file (the example will use `pipelines.py`) under any of the Django modules (either under an app folder or project folder):

This example has `mysite` as the project directory and `pipelines.py` as the module. Inside the file add up the needed Pyot Settings. The below example settings is AN EXAMPLE, you can customize the Settings for your needs. Don't forget to activate the settings.

```python{20}
#mysite/pipelines.py

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
```python{8}
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
# Supposing the pyot settings file is at: mysite/pipelines.py

PYOT_SETTINGS = ['mysite.pipelines']
```
You can define multiple settings in different files if you want to keep 1 setting per app (supposing you have 1 app per game model).

## Synchronous Compatibility

The wrappers from `asgiref.sync` will be responsible for this.

Running async function in sync code:

```python
from asgiref.sync import async_to_sync

async def bar():
    pass

def foo():
    async_to_sync(bar)()
```

```python
from asgiref.sync import async_to_sync

@async_to_sync
async def bar():
    pass

def foo():
    bar()
```

Running sync function in async code:

```python
from asgiref.sync import sync_to_async

def bar():
    pass

async def foo():
    await sync_to_async(bar)()
```

```python
from asgiref.sync import sync_to_async

@sync_to_async
def bar():
    pass

async def foo():
    await bar()
```

For more info, please read [Django Asynchronous Support](https://docs.djangoproject.com/en/3.1/topics/async/).

On windows, it is possible to see `RuntimeError: Event loop is closed` throwing from the proactor pipeline. This is a [known issue](https://github.com/aio-libs/aiohttp/issues/4324). ***This will not affect your code from running, because the exception will be ignored.*** You can still fix this on Windows so that the warning is not printed, you can add the following code in the same file of your pyot settings:

```python
import platform

if platform.system() == 'Windows':
    from asyncio.proactor_events import _ProactorBasePipeTransport
    from pyot.utils.internal import silence_event_loop_closed
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
```
