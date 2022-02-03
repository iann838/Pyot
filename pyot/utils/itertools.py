from typing import Dict, TypeVar, Generic, List, Iterator
import pickle


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
        return (pickle.loads(pickle.dumps(obj)) for obj in self.objects)


frozen_generator = FrozenGenerator


def swapped_dict(dic: Dict[K, V]) -> Dict[V, K]:
    '''Swap keys and values of a dictionary'''
    return {v: k for k, v in dic.items()}
