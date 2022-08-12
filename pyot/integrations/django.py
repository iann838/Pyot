import warnings

from pyot.conf.utils import import_confs
from pyot.core.warnings import PyotConfWarning


try:
    from django.core.exceptions import ImproperlyConfigured
    try:
        from django.conf import settings

        conf_paths = settings.PYOT_CONFS
        DJANGO_ENABLED = True
    except ImproperlyConfigured:
        DJANGO_ENABLED = False
    except AttributeError:
        warnings.warn("Django install detected, but could not find `PYOT_CONFS` settings variable", PyotConfWarning)
        DJANGO_ENABLED = False
except (ImportError, ModuleNotFoundError, NameError):
    DJANGO_ENABLED = False


def activate():
    if DJANGO_ENABLED:
        import_confs(conf_paths)
