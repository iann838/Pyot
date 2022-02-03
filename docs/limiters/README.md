# Limiters

Rate limiting is an essential part of using the Riot Games API.

- Prevents requests hitting 429.
- Lowers the risk of being banned due to excessive 429s.

They are only used in the RiotAPI store, different rate limiters has different pros and cons.

Rate limiters are configured on the `rate_limiter` param of the store configuration, the configurable values of rate limiters are params in the `__init__` definition of each rate limiter. Similar to how stores are configured.

There are a few configurable values that exists across multiple rate limiters, they will be documented here.

* `limiting_share`: `float = 1`
  > Value from 0 to 1. Rate limiter will only allow requests up to `bucket_max * limiting_share` (e.g. 0.7 will result in only using 70% of the limit).

## Example config

```python
    # ... Other stores
    {
        "backend": "pyot.stores.riotapi.RiotAPI",
        "api_key": os.environ["RIOT_API_KEY"],
        "rate_limiter": {
            "backend": "pyot.limiters.redis.RedisLimiter",
            "limiting_share": 1,
            "host": "127.0.0.1",
            "port": 6379,
            "db": 0,
        }
    }
```
