# Mongo DB

- Type: <Badge text="Pyot Cache" vertical="middle" /> <Badge text="Sharding" type="error" vertical="middle" />
- Description: Store that uses Mongo NoSQL DBs as Caches. This cache provides high speed read/write in disk persistent storage, objects expirations are handled by Mongo's TTL indexes.

:::tip INFO ABOUT THIS STORE
This store is best for production environment due to its high speed, TTL indexes and mainly disk based storage. Built on top of Python Async Driver of MongoDB called [Motor](https://motor.readthedocs.io/en/stable/).

Multiple instances of MongoDB is allowed, DB level sharding is also possible by following the Mongo's docs for sharding and pass the necessary kwargs to the settings.

Objects are stored as bytes strings serialized by `pickle` due to faster performance than bson format, to get a cached object from the db without using pyot's pipeline, `pickle.loads()` is needed for deserializing to python dictionary and further able to jsonify. (The util function `pytify` from `pyot.utils` also works) 
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.MongoDB`
### Arguments:
> #### `db: str`
> Name of the database to be used.
>
> #### `host: str = '127.0.0.1'`
> Host of the Mongo DB instance.
>
> #### `port: int = 27017`
> Port of the Mongo DB instance.
>
> #### `expirations: Dict[str, Any] = None`
> Custom mapping for overriding the default expirations. For details and defaults refer to Pipeline > Store Bases > Expirations section.
>
> #### `log_level: int = 10`
> Set the log level for the store. Defaults to 10 (DEBUG level).
>
> #### `**kwargs` (Any Extra key value pair)
> Any extra Key : Value pair that is passed to the `motor.motor_asyncio.AsyncIOMotorClient` instance. Refer to its arguments at [motor documentation](https://motor.readthedocs.io/en/stable/).

## Cached Endpoints

All available endpoints defined in the [default expirations](/pipeline/expiration.html#default-expirations). Endpoints are also documented under each service store documentation.

## Example Usage

In your Pyot settings.

```python{3}
    # PIPELINE ...
        {
            "BACKEND": "pyot.stores.MongoDB",
            "DB": 'pyot_lol',
            "HOST": "127.0.0.1",
            "PORT": 27017,
            "LOG_LEVEL": 10,
            "EXPIRATIONS": {...},
        },
    # ....
```
