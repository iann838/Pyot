import os
import asyncio
import inspect
import importlib

from ast import literal_eval


def runtask(funcname: str, *args):
    args = list(args)
    for ind, arg in enumerate(args):
        try:
            args[ind] = literal_eval(arg)
        except ValueError:
            continue
    proj = os.environ.get('PYOT_PROJECT_MODULE')
    wsgi = importlib.import_module(proj + '.wsgi')
    func = wsgi.app.tasks[funcname]
    if inspect.isclass(func):
        try:
            func = func()
        except TypeError as e:
            if "__init__() missing" in str(e):
                raise TypeError(
                    f"'{funcname}.__init__()' should only initialize attributes and not use required arguments (arguments with default is allowed)"
                ) from e
    if not hasattr(func, "__call__"):
        raise TypeError(f"'{funcname}.__call__()' is not implemented")
    if asyncio.iscoroutinefunction(func.__call__) or asyncio.iscoroutinefunction(func):
        asyncio.run(func(*args))
    else:
        func(*args)


def runserver(location: str = None):
    if not location:
        location = "127.0.0.1:" + os.environ.get('PYOT_SERVER_PORT')
    proj = os.environ.get('PYOT_PROJECT_MODULE')
    wsgi = importlib.import_module(proj + '.wsgi')
    host, port = location.split(":")
    port = int(port)
    wsgi.app(host=host, port=port)


commands = {
    "runtask": runtask,
    "runserver": runserver,
}
