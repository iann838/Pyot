from . import integrations


integrations.django.activate()


def load_tests(loader, tests, pattern):
    '''There are no tests inside main module'''
