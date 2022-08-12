# MongoDB

- Type: Cache
- Description: Uses Mongo NoSQL DBs as Caches.

This store is best for production environment due to its high speed, TTL indexes and mainly disk based storage. Built on top of Python Async Driver of MongoDB [Motor](https://motor.readthedocs.io/en/stable/).

DB level sharding is possible by following the Mongo's docs for sharding and pass the necessary kwargs to the settings.

An extra installation is required: `pip install pyot[mongodb]`

## _class_ `MongoDB`

Backend: `pyot.stores.mongodb.MongoDB`

Definitions:

* `__init__`
  * `db`: `str`
    > Name of the database to be used.
  * `host`: `str = '127.0.0.1'`
    > Host of the Mongo DB instance.
  * `port`: `int = 27017`
    > Port of the Mongo DB instance.
  * `expirations`: `Dict[str, int | float | timedelta] = None`
  * `log_level`: `int = 0`
  * `**kwargs`
    > Any extra kwargs provided will passed into `motor.motor_asyncio.AsyncIOMotorClient`. e.g. authentication params.
