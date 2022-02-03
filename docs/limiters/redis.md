# RedisLimiter

- Description: Redis based rate limiter.

Pros:

- Redis is a relatively fast key-value storage.
- Stateless, the state is stored in a redis server that can be accessed across processes.

Cons:

- Although minimal, latency exists when the redis server is on another machine.

{% hint style='info' %}
This rate limiter is built using aioredis v1.3, it does not support aioredis v2+ since it went through massive rework of all interfaces. A future rate limiter called `RedisLimiterV2` will be added with support for aioredis v2+.
{% endhint %}

An extra installation is required: `pip install pyot[redis]`

## _class_ RedisLimiter

Backend: `pyot.limiters.redis.RedisLimiter`

Definitions:

* `__init__`
  * `host`: `str = '127.0.0.1'`
    > Host of Redis.
  * `port`: `int = 6379`
    > Port of Redis.
  * `db`: `int = 0`
    > Database number of Redis.
  * `limiting_share`: `int = 1`
