# RedisCache

- Type: Cache
- Description: Uses Redis servers as Caches. This cache provides similar speeds to Omnistone while preserving data even if the program is down.

This Cache is built on top of Async Python integration of [redis](https://github.com/redis/redis-py).

An extra installation is required: `pip install pyot[redis]`

## _class_ `RedisCache`

Backend: `pyot.stores.rediscache.RedisCache`

Definitions:

* `__init__`
  * `host`: `str = '127.0.0.1'`
    > Host of Redis.
  * `port`: `int = 6379`
    > Port of Redis.
  * `db`: `int = 0`
    > Database number of Redis.
  * `expirations`: `Dict[str, int | float | timedelta] = None`
  * `log_level`: `int = 0`
  * `**kwargs`
    > Any extra kwargs provided will passed into `aioredis.Redis`. e.g username and password.
