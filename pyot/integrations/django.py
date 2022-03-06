from importlib import import_module
import warnings

try:
    from django.core.exceptions import ImproperlyConfigured
    try:
        from django.conf import settings

        try:
            paths = settings.PYOT_CONFS
        except AttributeError:
            paths = settings.PYOT_SETTINGS
            warnings.warn("'PYOT_SETTINGS' is deprecated in favor of 'PYOT_CONFS'", DeprecationWarning)
        DJANGO_ENABLED = True
    except ImproperlyConfigured:
        DJANGO_ENABLED = False
except (ImportError, ModuleNotFoundError, NameError):
    DJANGO_ENABLED = False


def activate():
    if DJANGO_ENABLED:
        for path in paths:
            import_module(path)
