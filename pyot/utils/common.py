from functools import partial
from inspect import getmembers, isfunction
from typing import List, Any, Set, Dict, TypeVar, Callable, Awaitable, ByteString, Optional, Type
from importlib import import_module
import itertools
import asyncio
import pickle
import re


T = TypeVar("T")
R = TypeVar("T")


def loop_run(coro: Awaitable[R]) -> R:
    '''Run the coroutine in the current event loop or a new one if `set_event_loop()` has not yet been called.'''
    return asyncio.get_event_loop().run_until_complete(coro)


async def thread_run(func: Callable[..., R], *args, **kwargs) -> R:
    '''Run a blocking function in a thread.'''
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))


def inherit_docstrings(cls):
    for name, func in getmembers(cls, isfunction):
        if func.__doc__: continue
        for parent in cls.__mro__[1:]:
            if hasattr(parent, name):
                func.__doc__ = getattr(parent, name).__doc__
    return cls


def case_combinations(string: str) -> Set[str]:
    return set(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in string))))


def case_insensitive_dict(dic: Dict) -> Dict:
    new_dic = {}
    for key, val in dic.items():
        for ikey in case_combinations(key):
            new_dic[ikey] = val
    return new_dic


def snakecase(attr: str) -> str:
    '''Convert string to python snakecase.'''
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attr)
    snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    return snake_case


def camelcase(snake_str: str) -> str:
    '''Convert string to json camelcase.'''
    components = snake_str.split('_')
    if len(components) == 1:
        return components[0]
    return components[0] + ''.join(x.title() for x in components[1:])


def shuffle_list(li: List[T], param: str, size: int = 10) -> List[T]:
    '''
    Shuffle a list by a specified param and chunk size.\n
    `param`: param to shuffle based on, either the an attribute or key.\n
    `size`: size of the returned chunks, e.g. `size=10` will return a new list with items of the same `param` every 10 items.\n
    Typically used for mixing pyot objects regions and platforms to better regulate rate limits.
    '''
    if size < 1:
        raise RuntimeError('size must be an integer greater than 0')
    groups = {}
    for obj in li:
        try:
            key = obj[param]
        except TypeError:
            key = getattr(obj, param)
        try:
            chunks = groups[key]
        except KeyError:
            groups[key] = [[]]
            chunks = groups[key]
        if len(chunks[-1]) < size:
            chunks[-1].append(obj)
        else:
            chunks.append([obj])
    new_list = []
    while len(groups) > 0:
        groups = {name: group for (name, group) in groups.items() if len(group) > 0}
        for name in groups:
            new_list += groups[name].pop(0)
    return new_list


def import_class(path: str) -> Any:
    '''Return the class given its python path'''
    store_cls_name = path.split('.')[-1]
    store_path = '.'.join(path.split('.')[:-1])
    module = import_module(store_path)
    store_cls = getattr(module, store_cls_name)
    if isinstance(store_cls, Exception):
        raise store_cls
    return store_cls


def fast_copy(obj: T) -> T:
    '''30x faster copy than `copy.deepcopy`, not all objects can be copied.'''
    return pickle.loads(pickle.dumps(obj, protocol=-1))


def bytify(obj) -> ByteString:
    '''Convert a python object to byte string.'''
    return pickle.dumps(obj)


def pytify(obj, class_of_t: Optional[Type[T]] = None) -> T:
    '''Convert a byte string to python object.'''
    return pickle.loads(obj)


def dict_key_value_swap(dic: Dict) -> Dict:
    '''Swap keys and values of a dictionary'''
    return {v: k for k, v in dic.items()}
