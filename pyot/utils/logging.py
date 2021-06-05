from logging import Logger as ILogger


class Logger(ILogger):
    '''Lazy logger which its `log()` method will do nothing if level == 0'''

    def __init__(self, name):
        super().__init__(name)

    def log(self, level, msg):
        '''I will do nothing if level == 0'''
        if level == 0:
            return
        super().log(level, msg)
