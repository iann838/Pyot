from importlib import import_module
from typing import Dict, List, Tuple, Type, Union
from types import FunctionType, ModuleType
import inspect

from pyot.core.objects import PyotStaticBase


def get_forward_refs(model_name: str) -> Dict[str, Union[PyotStaticBase, ModuleType]]:
    classes = {}

    model = import_module(f"pyot.models.{model_name}")
    for attr in list(filter(lambda att: not att.startswith("__"), dir(model))):
        classes[attr] = getattr(model, attr)
    return classes


def get_module_locals(o: Type):
    classes = {}

    module = inspect.getmodule(o)
    for attr in list(filter(lambda attr: not attr.startswith("__"), dir(module))):
        classes[attr] = getattr(module, attr)
    return classes


def get_properties(o: PyotStaticBase) -> List[Tuple[str, FunctionType]]:
    return inspect.getmembers(o.__class__, predicate=lambda func: isinstance(func, property))
