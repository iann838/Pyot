# Redis Cache

- Type: <Badge text="Pyot Cache" vertical="middle" /> <Badge text="Sharding" type="error" vertical="middle" />
- Description: Store that uses Redis servers as Caches. This cache provides similar speeds to Omnistone while preserving data even if the pipeline is down.

:::tip INFO ABOUT THIS STORE
The Cache is built on top of Python integration of [redis](https://pypi.org/project/redis/).

You can add multiple stores of this type to the pipeline, but take in mind that this store lives on RAM (hence the speed) so it might be limited if you want to cache bigger or more objects.
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.RedisCache`
### Arguments:
> #### `host: str = '127.0.0.1'`
> Host of the Redis server.
>
> #### `port: int = 6379`
> Port of the Redis server.
>
> #### `db: int = 0`
> Database of the Redis server.
>
> #### `expirations: Dict[str, Any] = None`
> Custom mapping for overriding the default expirations. For details and defaults refer to Pipeline > Store Bases > Expirations section.
>
> #### `log_level: int = 20`
> Set the log level for the store. Defaults to 20 (INFO level).
>
> #### `**kwargs` (Any Extra key value pair)
> Any extra Key : Value pair that is passed to the `redis.Redis` instance. Refer to its arguments at [redis documentation](https://redis-py.readthedocs.io/en/stable/).

## Cached Endpoints

All available endpoints defined in the default expirations.

## Example Usage

In your Pyot settings.

```python{3}
    # PIPELINE ...
        {
            "BACKEND": "pyot.stores.RedisCache",
            "HOST": "127.0.0.1",
            "PORT": 6379,
            "DB": 1,
            "EXPIRATIONS": {...},
        },
    # ....
```
