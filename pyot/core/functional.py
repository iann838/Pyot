from typing import Dict, Union
from functools import partial, wraps

from pyot.utils.common import camelcase
from .exceptions import NotFound


class lazy_property:
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance and inserted into the meta data dict using camelcase key.
    A cached property can be made out of an existing method:
    (e.g. ``url = lazy_property(get_absolute_url)``).
    """
    name = None

    @staticmethod
    def func(instance): # pylint: disable=method-hidden
        raise TypeError(
            'Cannot use cached_property instance without calling '
            '__set_name__() on it.'
        )

    def __init__(self, func, name=None):
        self.real_func = func
        self.key = camelcase(func.__name__)
        self.__doc__ = getattr(func, '__doc__')

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
            self.func = self.real_func
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." % (self.name, name)
            )

    def __get__(self, instance, cls=None):
        """
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        if instance is None:
            return self
        res = instance._meta.data[self.key] = instance.__dict__[self.name] = self.func(instance)
        return res


class cache_indexes:

    def __init__(self, func):
        self.indexes = {}
        self.func = func

    def __get__(self, instance, cls=None):
        return partial(self.__call__, instance)

    def __call__(self, instance, data):
        try:
            return self.func(instance, self, data)
        except KeyError:
            raise NotFound("Request was successful but filtering gave no matching item")

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
