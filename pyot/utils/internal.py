from .decorators import silence_event_loop_closed


def silence_proactor_pipe_deallocation():
    '''Silences the Exception `RuntimeError: Event loop is closed` in `_ProactorBasePipeTransport.__del__`.'''
    from asyncio.proactor_events import _ProactorBasePipeTransport
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
