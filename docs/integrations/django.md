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

## Views

{% hint style='danger' %}
If wsgi is used (unsure about asgi), it is forced to run async views in threads, make sure to use resource managers for graceful handling of resources, refer to **Cores -> Resources**.
{% endhint %}

```python
from django.views import View
from asgiref.sync import async_to_sync
from pyot.core.resources import resource_manager

@resource_manager.as_decorator
async def function_based_view_using_decorator(request):
    ...

async def function_based_view_using_context_manager(request):
    async with resource_manager():
        ...

class ClassBasedDecoratedView(View):
    @resource_manager.as_decorator
    async def get(self, request):
        ...

class ClassBasedContextManagedView(View):
    async def get(request):
        async with resource_manager():
            ...
```
