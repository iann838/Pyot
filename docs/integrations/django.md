# Django

Integration with Django.

## Setup

1. Set up Django project.
2. Create a file (generally called `pyotconf.py`) under any project module.
3. Configure the models and pipelines inside this file.
4. Add `pyot` to the `INSTALLED_APPS` of the project `settings.py` file.
5. Add the file path of the configuration file to a new `settings.py` variable `PYOT_CONFS` (list or iterable).

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

```python
PYOT_CONFS = ['mysite.pyotconf.py']
```

{% hint style='info' %}
The variable `PYOT_CONFS` can accept multiple files in case configurations are organized in separated files.
{% endhint %}

{% hint style='danger' %}
The old variable `PYOT_SETTINGS` is deprecated and will be removed in future versions.
{% endhint %}

## Synchronous Compatibility

Django provides wrappers from `asgiref.sync` to achieve this.

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

For more info, please refer to [Django Asynchronous Support](https://docs.djangoproject.com/en/dev/topics/async/).

{% hint style='danger' %}
If wsgi is used instead of asgi, errors like `RuntimeError: Event loop is closed` may appear, to fix this please refer to **Issues > RuntimeError -> Threading**. 
{% endhint %}
