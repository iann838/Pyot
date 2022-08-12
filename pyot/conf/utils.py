
from typing import List, Mapping, TypeVar, Type, Union
from importlib import import_module


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


def import_confs(path_or_paths: Union[str, List[str]]):
    if isinstance(path_or_paths, str):
        import_module(path_or_paths)
    elif isinstance(path_or_paths, list):
        for path in path_or_paths:
            import_module(path)
    else:
        raise ValueError(path_or_paths)
