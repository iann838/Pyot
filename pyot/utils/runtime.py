from functools import wraps
from typing import Callable


def silence_event_loop_closed(func: Callable):
    '''Silences the Exception `RuntimeError: Event loop is closed` in a class method.'''
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


def silence_proactor_pipe_deallocation():
    '''Silences the Exception `RuntimeError: Event loop is closed` in `_ProactorBasePipeTransport.__del__`.'''
    from asyncio.proactor_events import _ProactorBasePipeTransport
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
