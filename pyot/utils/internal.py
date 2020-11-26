from functools import wraps

def silence_event_loop_closed(func):
    '''Silences the Exception `RuntimeError: Event loop is closed` in a class method.'''
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper
