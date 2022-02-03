# Stores

Configuration documentations for all available stores in Pyot.

Each store is configured at pipeline definition, the configurable values of stores are the params in the `__init__` definition of each store. For example if a store can take `host` and `db` in the `__init__` method, it can be configured in the pipeline like this:
```python
    # ... Other stores
    {
        "backend": "pyot.stores.x.y",
        "host": "somehost",
        "db": "somedb"
    }
```

There are a few configurable values that exists across multiple stores, they will be documented here.

* `log_level`: `int = 0`
  > Used in all stores. Defines the log level of the logger used in the store, these uses the level specified in the [Python logging facilities](https://docs.python.org/3/library/logging.html#logging-levels), along with an extra level `0` which completely ignores the logging process. Defaults to `0`.

* `expirations`: `Dict[int, int | float | timedelta] = None`
  > Used in cache stores. Detailed documentations in **Pipeline > Expirations**.

* `error_handler`: `Dict[int, Tuple[int]] = None`
  > Used in services stores. Detailed documentations in **Pipeline > Handler**.
