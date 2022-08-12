import inspect
from typing import Any, List, Type


def get_method_properties(clas: Type[object]) -> List[str]:
    return inspect.getmembers(clas, predicate=lambda func: (
        (
            inspect.isfunction(func) and
            func.__name__ in clas.__dict__
        ) or (
            isinstance(func, property) and
            func.fget and
            func.fget.__name__ in clas.__dict__
        ) or (
            inspect.ismethod(func) and
            func.__name__ in clas.__dict__ and
            isinstance(clas.__dict__[func.__name__], (classmethod, staticmethod))
        )
    ))


def get_method_property_names(clas: Any) -> List[str]:
    return [i[0] for i in inspect.getmembers(clas, predicate=lambda func: inspect.isfunction(func) or isinstance(func, property))]


def newline_join(any):
    return '\n'.join(any)
