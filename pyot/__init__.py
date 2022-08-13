from . import integrations

__version__ = "6.0.1"


integrations.django.activate()


def load_tests(loader, tests, pattern):
    '''There are no tests inside main module'''
