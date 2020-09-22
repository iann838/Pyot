# Redis Limiter

Rate limiter based on Redis. This Rate Limiter is async safe, thread safe, **_cross-process safe and also api-key safe (meaning merged keys are safe without doing limiting share)_**.

Limits on the db are expired after 1 hour if it isn't touched.

## Rate Limiter Settings Reference
### Backend: `pyot.limiters.RedisLimiter`
### Arguments:
> #### `limiting_share: float = 1`
> The amount of rate limits * `limiting_share` to use at most, receives a float between 0 and 1. Defaults to 1.
> #### `host: str = '127.0.0.1'`
> Host of the Redis Server.
> #### `port: int = 6379`
> Port of the Redis Server.
> #### `db: int = 0`
> Database of the Redis Server, preferably separated from your cache.
> #### `**kwargs` (Any Extra key value pair)
> Any extra Key : Value pair that is passed to the `redis.Redis` instance. Refer to its arguments at [redis documentation](https://redis-py.readthedocs.io/en/stable/).

## Example Usage

```python
{
    "BACKEND": "pyot.stores.RiotAPI",
    "RATE_LIMITER": {
        "BACKEND": "pyot.limiters.RedisLimiter",
        "LIMITING_SHARE": 1,
        "HOST": "127.0.0.1",
        "PORT": 6379,
        "DB": 0,
    },
}
```
