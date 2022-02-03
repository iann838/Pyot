from logging import Logger as ILogger


class Logger(ILogger):
    '''Lazy logger which its `log()` method will do nothing if level equals 0'''

    def __init__(self, name):
        super().__init__(name)

    def log(self, level, msg):
        '''Same as logging.Logger.log, with a new level (0) to skip logging.'''
        if level == 0:
            return
        super().log(level, msg)
