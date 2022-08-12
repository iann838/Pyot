# DiskCache

- Type: Cache
- Description: Uses Disk files (and SQLite DBs) as Caches. Takes advantage of the disk space instead of RAM.

This Cache is built on top of [diskcache](http://www.grantjenks.com/docs/diskcache/index.html) on its `FanoutCache`.

An extra installation is required: `pip install pyot[diskcache]`

## _class_ `DiskCache`

Backend: `pyot.stores.diskcache.DiskCache`

Definitions:

* `__init__`
  * `directory`: `str | Path`
    > Path of the directory used as cache.
  * `expirations`: `Dict[str, int | float | timedelta] = None`
  * `log_level`: `int = 0`
  * `**kwargs`
    > Any extra kwargs provided will be passed into `diskcache.FanoutCache`.
