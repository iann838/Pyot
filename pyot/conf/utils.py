import re
from typing import Mapping, TypeVar, Type


K = TypeVar("K")
V = TypeVar("V")


class ConfDict(dict, Mapping[K, V]):

    def __init__(self, cls: Type[V], throw: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.throw = throw

    def __getattr__(self, k: K) -> V:
        try:
            return self[k]
        except KeyError as e:
            if self.throw:
                raise AttributeError(self.throw.format(k)) from e
            return None

    def __setattr__(self, name: str, value: V) -> None:
        self[name] = value


def reraise_model_inactive(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise RuntimeError("Model partially activated") from e

    return wrapper


def valid_attribute_key(key: str):
    return bool(re.match(r"^([a-zA-Z_])([a-zA-Z0-9_]*)$", key))
