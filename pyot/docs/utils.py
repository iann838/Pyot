import inspect
from typing import Any, List


def get_method_properties(clas: Any) -> List[str]:
    return inspect.getmembers(clas, predicate=lambda func: inspect.isfunction(func) or isinstance(func, property))


def get_method_property_names(clas: Any) -> List[str]:
    return [i[0] for i in inspect.getmembers(clas, predicate=lambda func: inspect.isfunction(func) or isinstance(func, property))]


def newline_join(any):
    return '\n'.join(any)
