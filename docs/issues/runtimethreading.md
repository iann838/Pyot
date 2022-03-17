# RuntimeError > Threading

Severity: Minimal (Does not break code)

In general some problems may appear when threading and asyncio is used together, and sometimes its inevitable (e.g. A web framework only supports wsgi).

When threading is used, Pyot will automatically create isolated copies of resources for each unique event loop (each thread runs a single different event loop). Internally Pyot can only save up to 128 copies per factory, the moment it passes that amount, it will aggressively trigger a culling process. This is where problems are, the factories will attempt to **close and deallocate the resources on event loops that are already closed**, most of these closing calls are asynchronous and are bound to the event loop that spawned it, these factories has no reliable way to know _when_ an event loop is closed. Thus, a bunch of exceptions may start appearing such as `RuntimeError: Event loop is closed`. These exceptions does not break the code, because these exceptions are raised out of stack and ignored, **if otherwise, it's not related to this issue**.

## Solution

Use the atomic resource manager wrapper. This manager tells where exactly resources will be used in an event loop and does proper setups and cleanups of these resources. **Only one instance** at most should be in action at any moment in an **event loop**.

```python
from pyot.utils.eventloop import resource_manager

@resource_manager.atomic
async def some_func():
    # ...
```

{% hint style='info' %}
Generally only the **top most async function** is wrapped. For example:
- Projects main function.
- Django's wsgi views methods and functions.
- Functions passed to concurrent executors.
{% endhint %}

If the function is wrapped by `async_to_sync`, it must be placed above.
```python
@async_to_sync
@resource_manager.atomic
async def some_func():
    # ...
```

{% hint style='danger' %}
Wrapped functions must not:
- Execute others similarly wrapped functions.
- Run concurrently in the the same event loop.

If these situations surfaces, consider:
- Moving the decorator to an outer scope.
- Make the outer scope function async and move the decorator there.
- Reworking the code structure to fix the conflict.
{% endhint %}
