# Default task manager for pyot projects.
# Feel free to change this file to your wanted behavior.

import sys
import asyncio

# Loads declared callables
from . import tasks


def execute_task_from_args():
    try:
        funcname = sys.argv[1]
        args = sys.argv[2:] if len(sys.argv) > 2 else []
    except IndexError as e:
        raise Exception('Missing callable name for execution') from e
    func = getattr(tasks, funcname)
    if asyncio.iscoroutinefunction(func):
        asyncio.run(func(*args))
    else:
        func(*args)
