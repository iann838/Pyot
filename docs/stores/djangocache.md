# DjangoCache

- Type: Cache
- Description: Uses production tested caches of the Django Cache Framework.

This store is intended for projects built with Django. It can be used with **any** cache of Django. The configuration of this cache is only an alias to the configuration in Django's project settings.

## _class_ `DjangoCache`

Backend: `pyot.stores.djangocache.DjangoCache`

Definitions:

* `__init__`
  * `alias`: `str`
    > The alias of the Django Cache defined in the `CACHES` variable of `settings.py` (specifically these are the dictionary keys of `CACHES`).
  * `expirations`: `Dict[str, int | float | timedelta] = None`
  * `log_level`: `int = 0`
