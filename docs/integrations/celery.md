# Celery

Integration with Celery.

## Setup

1. Set up Celery project.
2. Configure pyot models and pipelines.

## Synchronous Compatibility

Celery does not support async functions, a simple utility decorator is provided.

```python
from pyot.utils.sync import async_to_sync
from .celery import app

@app.task
@async_to_sync
async def mytask():
    # ...
```

{% hint style='danger' %}
If wsgi is used instead of asgi, errors like `RuntimeError: Event loop is closed` may appear, to fix this please refer to **Issues > RuntimeError > Threading**. 
{% endhint %}
