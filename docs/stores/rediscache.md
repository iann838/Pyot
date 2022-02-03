# RedisCache

- Type: Cache
- Description: Uses Redis servers as Caches. This cache provides similar speeds to Omnistone while preserving data even if the program is down.

This Cache is built on top of Async Python integration of [redis](https://github.com/aio-libs/aioredis-py).

{% hint style='info' %}
This store is built using aioredis v1.3, it does not support aioredis v2+ since it went through massive rework of all interfaces. A future store called `RedisCacheV2` will be added with support for aioredis v2+.
{% endhint %}

An extra installation is required: `pip install pyot[redis]`

## _class_ RedisCache

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
  * `kwargs`: `Dict[str, Any]`
    > Extra kwargs to be passed to `aioredis.create_redis_pool`.
