from typing import Callable, Any, TypeVar
from collections import defaultdict
from django.core.cache import caches
import datetime

from logging import getLogger

LOGGER = getLogger(__name__)
T = TypeVar("T")

class DjangoCache(object):
    def __init__(self, alias: str = None, logs_enabled: bool = False) -> None:
        self._alias = alias
        self._cache = caches[alias]
        self._logs_enabled = logs_enabled

    def put(self, key: Any, value: Any, timeout: int = -1) -> None:
        if timeout != 0:
            if timeout == -1:
                timeout = None
            self._cache.set(key, value, timeout)
            if self._logs_enabled:
                LOGGER.warn(f"[Trace: {self._alias}] PUT: {key}")

    def put_many(self, pairs: Any, timeout: int = -1) -> None:
        if timeout != 0:
            if timeout == -1:
                timeout = None
            self._cache.set_many(pairs, timeout)
            if self._logs_enabled:
                LOGGER.warn(f"[Trace: {self._alias}] PUT-MANY: {[key for key in pairs.keys()]}")

    def get(self, key: Any) -> Any:
        item = self._cache.get(key)
        if item is None:
            raise KeyError
        if self._logs_enabled:
            LOGGER.warn(f"[Trace: {self._alias}] GET: {key}")
        return item

    # This varies from the cache backend you use, might implement
    def get_all(self, type: Any):
        raise NotImplementedError

    # This should be rarely used, no delete() implemented in cassiopeia
    # You need to manually enter the key
    # For django you can just simply delete it by entering your cache backend server/db
    def delete(self, key: Any) -> None:
        self._cache.delete(key)

    # Again, cass not implemented, you can do it on your django backend server/db
    # but option is here if you want to make life harder
    def contains(self, key: Any) -> bool:
        item = self._cache.get(key)
        if item is None:
            return False
        return True
    
    # This function is really not needed.
    # It is more than a helper func if you're not familiar with django cache.
    # Django way of clearing:
    # terminal/cmd: `python manage.py shell`
    # >>> from django.core.cache import caches
    # >>> caches[name_of_your_cache].clear()
    def clear(self, pref: str = None):
        if pref is None:
            self._cache.clear()
        else:
            self._cache.clear(prefix=pref)

    # No need to expire, Django handles it.
    # For filebased/database backends, it should have its own culling system.
    def expire(self, type: Any = None):
        pass

