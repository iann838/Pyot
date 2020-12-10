# Omnistone

- Type: <Badge text="Pyot Cache" vertical="middle" />
- Description: A temporary Cache that starts on Pyot Settings activation and shut down on script or server exit. Since it lives at runtime it is a lot faster than an independent Cache server.

:::tip INFO ABOUT THIS STORE
This Cache doesn't expire data after it _expired_, to prevent memory overflow, a cull system is in place, when the amount of data reaches a limit, it calls the `expire()` coroutine on its own, if the amount of data is still higher than `MAX_ENTRIES` * (1 - 1/`CULL_FRECUENCY`), then it deletes items until the set amount, deletion prioritizes least recently used data.
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.Omnistone`
### Arguments:
> #### `expirations: Dict[str, Any] = None`
> Custom mapping for overriding the default expirations. For details and defaults refer to Pipeline > Store Bases > Expirations section.
>
> #### `max_entries: int = 10000`
> The maximum amount of items to hold before expiring
>
> #### `cull_frecuency: int = 2`
> The 1/x ratio of max_entries to be culled in case it still passes this amount after expiring. Manual expiring will not trigger culling.
>
> #### `log_level: int = 10`
> Set the log level for the store. Defaults to 10 (DEBUG level).


## Cached Endpoints

All available endpoints defined in the [default expirations](/pipeline/expiration.html#default-expirations). Endpoints are also documented under each service store documentation.
