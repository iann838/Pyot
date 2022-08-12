# Celery

Integration with Celery.

## Setup

1. Set up Celery project.
2. Configure pyot models and pipelines.

```python
# Other imports ...
from pyot.conf.utils import import_confs

# Celery settings stuff ...

import_confs("<pyotconf_import_path>")
```

{% hint style='tip' %}
Import path is the path used as if the file/module is being imported using python syntax via `import`, `__import__` or `importlib.import_module`
{% endhint %}

## Tasks

Celery does not support async functions, a util wrapper is provided `async_to_sync` in `pyot.utils.sync` to convert async functions into blocking functions.

{% hint style='danger' %}
Celery runs tasks in threads or processes, make sure to use resource managers for graceful handling of resources, refer to **Cores -> Resources**.
{% endhint %}

```python
from pyot.core.resources import resource_manager
from pyot.utils.sync import async_to_sync

# ...

@app.task
@async_to_sync
@resource_manager.as_decorator
async def task_using_decorator():
    ...

# OR

@app.task
@async_to_sync
async def task_using_context_manager():
    async with resource_manager():
        ...
```
