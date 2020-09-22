# Django Cache

- Type: <Badge text="Pyot Cache" vertical="middle" /> <Badge text="Sharding" type="error" vertical="middle" />
- Description: Store that uses the Django Cache Low Level API to take advantage of the production tested caches backend of Django.

:::tip INFO ABOUT THIS STORE
You can use ANY cache of Django and plug it into Pyot.

You can add multiple stores of this type to the pipeline, but take in mind that this store is independent of the server, so it might be slower or faster depending the cache backend used.
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.DjangoCache`
### Arguments:
> #### `alias: str = None`
> The alias identifying the Django Cache defined in the `CACHES` variable of Django's `settings.py`, an example is provided below.
>
> #### `expirations: Dict[str, Any] = None`
> Custom mapping for overriding the default expirations. For details and defaults refer to Pipeline > Store Bases > Expirations section.
>
> #### `log_level: int = 20`
> Set the log level for the store. Defaults to 20 (INFO level).

## Cached Endpoints

All available endpoints defined in the default expirations.

## Example Usage

Django `settings.py`, highlighted lines are the "alias" that needs to be passed to DjangoCache.

```python{13,22}
# Example django cache config
CACHES = {
    # Leave the "default" cache for handling data for your apps (preferable)
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/10", #db:10 for test
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # Example cache for cass using "django-redis" (pip install)
    # Check Out "django-redis" repository/docs for lot more flexible configurations.
    "pyot-redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3", #db:3 for test
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1
        }
    },
    # Example cache using FileBased backend that stores a max of 10k values
    'pyot-filebased': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'filebased-cache',
        'MAX_ENTRIES': 10000,
    }
}
```

:::tip INFO
For more caching backends and/or configurations. Please check [Django's Cache Framework documentation](https://docs.djangoproject.com/en/3.1/topics/cache/).
:::

Then in your Pyot settings.

```python{4,8}
    # PIPELINE ...
        {
            "BACKEND": "pyot.stores.DjangoCache",
            "ALIAS": "pyot-redis",
        },
        {
            "BACKEND": "pyot.stores.DjangoCache",
            "ALIAS": "pyot-filebased",
        },
    # ....
```