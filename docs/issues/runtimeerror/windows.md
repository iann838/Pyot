# RuntimeError > Windows

Severity: Minimal (Does not break code)

On Windows, it is possible to have `RuntimeError: Event loop is closed` exceptions raising from proactor pipelines. This is a [known issue](https://github.com/aio-libs/aiohttp/issues/4324) and does not affect the code from running, because these exceptions are raised out of stack and ignored, **if otherwise, it's not related to this issue**.

## Solution

A helper function may fix this on Windows so that the warning is not printed, the following code can be added in the same place as the pyot confs:

```python
import platform

if platform.system() == 'Windows':
    from pyot.utils.runtime import silence_proactor_pipe_deallocation
    silence_proactor_pipe_deallocation()
```

{% hint style='danger' %}
This may not be only cause for this exception to raise out of flow, another cause could be the use of threads in Python combined with asyncio, the issue documentation with its solution is in another article.
{% endhint %}
