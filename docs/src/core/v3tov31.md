# Version 3.0 → 3.1

This guide **covers only backward imcompatible changes** and the necessary steps for migrating Pyot 2 to Pyot 3. For Pyot 3 release notes please head to releases.

## Changes

### Store `MongoDB` now only stores data as bson format.
> MongoDB is NOT compatible of v3.0, it now uses bson format for caching, after updating to v3.1, old items are automatically deleted progressively when accessed. To maintain old cached items, run the following in python shell with settings activated.
> ```python
> from pyot.migrate.mongodb import migrate_all_to_bson
> migrate_all_to_bson()
> ```
> Clearing the cache instead is the fastest approach without any hassle.
> ```python
> from pyot.pipeline import pipelines
> from pyot.stores import MongoDB
> from asyncio import run
>
> pipeline = pipelines[model]
> for store in pipeline:
>     if isinstance(store, MongoDB):
>         run(store.clear())
> ```


### `lol.CurrentGame` has been reworked.
> Full list of new / changed attributes are in the docs.

### `lol.Featured` has been reworked.
> Full list of new / changed attributes are in the docs.
