# Disk Cache

- Type: <Badge text="Pyot Cache" vertical="middle" /> <Badge text="Sharding" type="error" vertical="middle" />
- Description: Store that uses Disk files (and Sqlite dbs) as Caches. This cache takes advantage of the disk space instead of RAM.

:::tip INFO ABOUT THIS STORE
This Cache is built on top of (diskcache)[http://www.grantjenks.com/docs/diskcache/index.html] on its `FanoutCache` to support multiple reads one write scheme to ensure speed.

You can add multiple stores of this type to the pipeline, but take in mind that this store lives on RAM (hence the speed) so it might be limited if you want to cache bigger or more objects.
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.DiskCache`
### Arguments:
> #### `directory: Union[str, pathlib.Path] = None`
> Directory of the Cache, it can accept a `pathlib.Path` object or a string to the directory.
>
> #### `expirations: Dict[str, Any] = None`
> Custom mapping for overriding the default expirations. For details and defaults refer to Pipeline > Store Bases > Expirations section.
>
> #### `log_level: int = 20`
> Set the log level for the store. Defaults to 20 (INFO level).
>
> #### `**kwargs` (Any Extra key value pair)
> Any extra Key : Value pair that is passed to the `diskcache.FanoutCache` instance. Refer to its arguments at [diskcache documentation](http://www.grantjenks.com/docs/diskcache/api.html).

## Cached Endpoints

All available endpoints defined in the default expirations.

## Example Usage

In your Pyot settings.

```python{3}
    # PIPELINE ...
        {
            "BACKEND": "pyot.stores.DiskCache",
            "DIRECTORY": Path.cwd() / 'diskcache',
        },
    # ....
```
