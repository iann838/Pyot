from typing import TypeVar, Generic, List, Iterator

from .copy import fast_copy


T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class FrozenGenerator(Generic[T]):
    '''
    Generator that isolates the original list by returning copies of objects when iterated.
    Used for preventing memory leaks of self-filled objects at the cost of performance.
    '''

    def __init__(self, li: List[T]):
        self.objects = li

    def __iter__(self) -> Iterator[T]:
        return (fast_copy(obj) for obj in self.objects)


frozen_generator = FrozenGenerator
