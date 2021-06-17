from typing import Any, TypeVar


T = TypeVar("T")


class NullSafe:

    def __getattr__(self, k: str):
        return NullSafe()

    def __getitem__(self, k: str):
        try:
            return self.__dict__[k]
        except KeyError:
            return NullSafe()

    def __setitem__(self, k: str, v: Any):
        self.__dict__[k] = v

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return None

    def __bool__(self):
        return False

    def __eq__(self, o: object) -> bool:
        if o is None or isinstance(o, NullSafe):
            return True
        return False

    def __repr__(self) -> str:
        return "NullSafe"

    def __str__(self) -> str:
        return "NullSafe"

    def __int__(self) -> int:
        return 0

    def __iter__(self):
        return iter([])

    def __len__(self) -> int:
        return 0


def nullsafe(o: T) -> T:
    return o or NullSafe()
