from importlib import import_module

try:
    from django.core.exceptions import ImproperlyConfigured
    try:
        from django.conf import settings

        paths = settings.PYOT_SETTINGS
        DJANGO_ENABLED = True
    except ImproperlyConfigured:
        DJANGO_ENABLED = False
except (ImportError, ModuleNotFoundError, NameError):
    DJANGO_ENABLED = False


if DJANGO_ENABLED:
    for path in paths:
        import_module(path)


def load_tests(loader, tests, pattern):
    '''There are no tests inside main module'''
