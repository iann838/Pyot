# FastAPI

Integration with FastAPI.

## Setup

1. Setup FastAPI project.
2. Configure pyot models and pipelines.
3. Import conf file in startup event.

```python
# Other imports ...
from pyot.conf.utils import import_confs

# FastAPI stuff ...

@app.on_event("startup")
async def startup_tasks():
    import_confs("<pyotconf_import_path>")
```

{% hint style='tip' %}
Import path is the path used as if the file/module is being imported using python syntax via `import`, `__import__` or `importlib.import_module`
{% endhint %}
