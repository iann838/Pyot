from . import core, pipeline, utils, models, limiters, stores

try:
    from django.core.exceptions import ImproperlyConfigured
    try:
        from django.conf import settings
        from importlib import import_module
        
        paths = settings.PYOT_SETTINGS
        
        for path in paths:
            import_module(path)
    except ImproperlyConfigured:
        pass
except (ImportError, ModuleNotFoundError, NameError): pass
