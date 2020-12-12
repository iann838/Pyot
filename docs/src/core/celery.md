# Celery

Celery is a Task Queue for scheduling tasks and workloads.

You probably don't need celery for concurrency, since the Pyot itself gives you high concurrency. In most scenarios you will need celery for distributing work across multiple processes or machines, which in Python it can become tricky with `multiprocessing` and periodic tasks that can also get tricky with normal cronjobs.

Example usage:
* Run a task every day at 4 AM.
* Run multiple CPU intense tasks at the same time in a multicore machine
* Run the same task on multiple machines.

Celery itself supports Django.

First you need to follow the [celery setup guide](https://docs.celeryproject.org/en/stable/getting-started/introduction.html).

After that, all you need to do is import the celery instance and decorate it as needed.

## Asyncio Issues

Celery does not support async functions, there is 2 solution.

### Using AsyncToSync decorator

```shell
pip install asgiref
```
Wrap the tasks

```python
from asgiref.sync import async_to_sync
from .celery import app

@app.task
@async_to_sync
async def mytask():
    # ...
```

### Calling asyncio.run 

Using asyncio.run involves in creating a proxy synchronous function, which is not so clean. You can also create a decorator that functions similarly to `async_to_sync`.

```python
import asyncio
from .celery import app

async def mytask():
    # ...

@app.task
def my_proxy_task():
    asyncio.run(mytask())
```

