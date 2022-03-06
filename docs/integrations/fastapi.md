# FastAPI

Integration with FastAPI.

## Setup

1. Setup FastAPI project.
2. Configure pyot models and pipelines.

Or alternatively:

2. Create a file (generally called `pyotconf.py`) under any project module.
3. Configure the models and pipelines inside this file.
4. Import this file in startup event.

```python
@app.on_event("startup")
async def startup_tasks():
    from . import pyotconf
```
