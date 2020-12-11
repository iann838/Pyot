# RuntimeError: Event loop is closed

On windows, it is possible to see `RuntimeError: Event loop is closed` throwing from the proactor pipeline. This is a [known issue](https://github.com/aio-libs/aiohttp/issues/4324). ***This will not affect your code from running, because the exception will be ignored.*** You can still fix this on Windows so that the warning is not printed, you can add the following code in the same file of your pyot settings:

```python
import platform

if platform.system() == 'Windows':
    from pyot.utils.internal import silence_proactor_pipe_deallocation
    silence_proactor_pipe_deallocation()
```
