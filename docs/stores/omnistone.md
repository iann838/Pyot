# Omnistone

- Type: Cache
- Description: In-Memory Cache that lives for the lifetime of the project runtime. Since it lives in Python memory, it's the fastest cache.

This Cache doesn't expire data after it is _expired_. To prevent memory overflow, a cull system is in place. When the amount of data reaches a limit, it calls the `expire()` coroutine on its own. If the amount of data is still higher than `MAX_ENTRIES` * (1 - 1/`CULL_FRECUENCY`), it deletes items until its less than the limit. Deletion prioritizes least recently used data.

## _class_ `Omnistone`

Backend: `pyot.stores.omnistone.Omnistone`

Definitions:

* `__init__`
  * `max_entries: int = 10000`
    > The maximum amount of items to hold before expiring
  * `cull_frecuency: int = 2`
    > The 1/x ratio of max_entries to be culled. Manual expiring will not trigger culling.
  * `expirations`: `Dict[str, int | float | timedelta] = None`
  * `log_level`: `int = 0`
