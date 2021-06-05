from importlib import import_module


def load_module(path):
    try:
        args = path.split(".")
        return import_module(args[-1], ".".join(args[:-1]))
    except ModuleNotFoundError:
        return import_module(path)
