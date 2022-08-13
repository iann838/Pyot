# RedisLimiter

- Description: Redis based rate limiter.

Pros:

- Redis is a relatively fast key-value storage.
- Stateless, the state is stored in a redis server that can be accessed across processes.

Cons:

- Although minimal, latency exists when the redis server is on another machine.

An extra installation is required: `pip install pyot[redis]`

## _class_ `RedisLimiter`

Backend: `pyot.limiters.redis.RedisLimiter`

Definitions:

* `__init__`
  * `host`: `str = '127.0.0.1'`
    > Host of Redis.
  * `port`: `int = 6379`
    > Port of Redis.
  * `db`: `int = 0`
    > Database number of Redis.
  * `limiting_share`: `float = 1`
  * `**kwargs`
    > Any extra kwargs provided will passed into `aioredis.Redis`. e.g. username and password.
