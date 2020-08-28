from django.conf import settings
from importlib import import_module

paths = settings.PYOT_SETTINGS

for path in paths:
    import_module(path)