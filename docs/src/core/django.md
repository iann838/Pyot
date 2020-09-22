# Django

Plugging Pyot into Django is really easy.

:::danger DEPRECATED
Since v1.1.0: The module `djot` for Django has been removed, now `pyot` can be natively installed.
:::

## Installation

Create a file (the example will use `pyoter.py`) under any of the Django modules (either under an app folder or project folder):

This example has `test` as the project directory and `pyoter.py` as the module. Inside the file add up the needed Pyot Settings. The below example settings is AN EXAMPLE, you can customize the Settings for your needs. Don't forget to activate the settings.

```python{11}
#test/pyoter.py

from pyot.core import Settings
from datetime import timedelta as td
import os

Settings(
    MODEL = "LOL",
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN_US",
    PIPELINE = [
        {"BACKEND": "pyot.stores.Omnistone"},
        {"BACKEND": "pyot.stores.MerakiCDN"}
        {"BACKEND": "pyot.stores.CDragon"},
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "KEY": os.environ["RIOT_API_KEY"],
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
# Supposing the pyot settings file is at: test/pyoter.py

PYOT_SETTINGS = [
    'test.pyoter'
]
```
You can define multiple settings in different files if you want to keep 1 setting per app (supposing you have 1 app per game model).
