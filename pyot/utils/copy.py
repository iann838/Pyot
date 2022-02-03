from typing import TypeVar
import pickle


T = TypeVar("T")


def fast_copy(obj: T) -> T:
    '''30x faster copy than `copy.deepcopy`, but not all objects can be fast copied (e.g. lambdas).'''
    return pickle.loads(pickle.dumps(obj, protocol=-1))
