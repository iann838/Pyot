from typing import TypeVar
import pickle


T = TypeVar("T")


def fast_copy(obj: T) -> T:
    '''30x faster copy than `copy.deepcopy`, not all objects can be copied.'''
    return pickle.loads(pickle.dumps(obj, protocol=-1))
