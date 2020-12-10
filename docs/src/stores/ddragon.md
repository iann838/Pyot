# DDragon

- Type: <Badge text="Pyot Service" vertical="middle" />
- Models: <Badge text="LOR" type="error" vertical="middle" />
- Description: Store that provides data from the Official Data Dragon, this store provides the endpoints for the Pyot Core Objects that returns static data, a list of the endpoints is found below.

:::tip INFO ABOUT THIS STORE
DDragon only supports Legends of Runeterra endpoints (the only one well maintained), as you may already noticed, DDragon for LoL and TFT are badly maintained and considered low priority for the game team.
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.DDragon`
### Arguments:
> #### `error_handling: Mapping[int, Tuple[str, List[int]]] = None`
> Define how this store should handle request errors, please refer to [Error Handler](/pipeline/handler.html) documentations at Pipeline.
>
> #### `log_level: int = 10`
> Set the log level for the store. Defaults to 10 (DEBUG level).
>
> #### `version: str = 'latest'`
> Set the version to use for the requests. Defaults to `latest`.

## Endpoints

> ### `LOR` <Badge text="Model" type="warning" vertical="middle" />
>`"ddragon_lor_set_data"`

## Example Usage

```python
{
    "BACKEND": "pyot.stores.DDragon",
    "LOG_LEVEL": 30,
    "VERSION": "latest",
    "ERROR_HANDLING": {
        404: ("T", []),
        500: ("R", [3])
    }
},
```