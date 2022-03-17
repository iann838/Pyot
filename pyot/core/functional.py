from typing import Any, Dict, Union
from functools import partial, wraps

from pyot.utils.text import camelcase
from .exceptions import NotFound


class lazy_property(property):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance and inserted into the meta data dict using camelcase key.\n
    Can only be used on pyot class methods.
    """
    name = None

    @classmethod
    def func(cls, instance) -> Any:
        raise TypeError(
            f'Cannot use {cls.__class__.__name__} instance without calling '
            '__set_name__() on it.'
        )

    def __init__(self, func, name=None): # pylint: disable=super-init-not-called
        self.real_func = func
        self.key = camelcase(func.__name__)
        self.once = False
        self.__doc__ = getattr(func, '__doc__')

    def __set_name__(self, owner, name):
        from .objects import PyotStaticBase
        if not issubclass(owner, PyotStaticBase):
            raise TypeError('Cannot use lazy_property on non pyot class methods.')
        if self.name is None:
            self.name = name
            self.func = self.real_func
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same lazy_property to two different names "
                "(%r and %r)." % (self.name, name)
            )

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        if self.once:
            try:
                return instance._meta.data[self.key]
            except KeyError:
                pass
        self.once = True
        res = instance._meta.data[self.key] = instance.__dict__[self.name] = self.func(instance)
        return res

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")


class cache_indexes:

    def __init__(self, func):
        self.indexes = {}
        self.func = func

    def __get__(self, instance, cls=None):
        return partial(self.__call__, instance)

    def __call__(self, instance, data):
        try:
            return self.func(instance, self, data)
        except KeyError as e:
            raise NotFound("Request was successful but filtering gave no matching item") from e

    @staticmethod
    def _get_index(name, data, key):
        for ind, item in enumerate(data):
            if item[key] == name:
                return ind
        raise NotFound("Request was successful but filtering gave no matching item")

    def get(self, name: str, data: Dict, key: Union[str, int]):
        lazy_func = partial(self._get_index, name, data, key)
        ind = self._get(name, lazy_func)
        if data[ind][key] == name: # RETURN ONLY IF ID MATCHES
            return data[ind]
        ind = lazy_func()
        self._set(name, ind)
        return data[ind]

    def _get(self, name: str, func):
        '''Get an index'''
        try:
            return self.indexes[name]
        except KeyError:
            pass
        response = func()
        self._set(name, response)
        return response

    def _set(self, name: str, val):
        '''Set an index.'''
        self.indexes[name] = val
        return name

    def _clear(self):
        '''Clear indexes.'''
        self.indexes = dict()


def turbo_copy(data, top, level=0):
    if level >= top:
        return data
    if isinstance(data, dict):
        data = data.copy()
        for key, val in data.items():
            data[key] = turbo_copy(val, top, level+1)
    elif isinstance(data, list):
        data = data.copy()
        for key, val in enumerate(data):
            data[key] = turbo_copy(val, top, level+1)
    return data


def save_raw_response(func):
    @wraps(func)
    def wrapper(self, data, *args, **kwargs):
        self._meta.raw_data = turbo_copy(data, self._meta.turbo_level)
        return func(self, data, *args, **kwargs)
    return wrapper


def laziable(obj):
    if isinstance(obj, dict) or isinstance(obj, list):
        return True
    return False

def parse_camelcase(kwargs: Dict) -> Dict:
    return {camelcase(key): val for (key, val) in kwargs.items() if key != "self" and val is not None}


def handle_import_error(module: ImportError):
    if isinstance(module, (ImportError, ValueError)):
        def raise_when_called(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                raise module
            return wrapper
        return raise_when_called
    def decorate(func):
        return func
    return decorate
