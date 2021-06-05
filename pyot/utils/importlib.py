from typing import Any, TypeVar
from importlib import import_module


T = TypeVar("T")


def import_class(path: str) -> Any:
    '''Return the class given its python path'''
    store_cls_name = path.split('.')[-1]
    store_path = '.'.join(path.split('.')[:-1])
    module = import_module(store_path)
    store_cls = getattr(module, store_cls_name)
    if isinstance(store_cls, Exception):
        raise store_cls
    return store_cls
