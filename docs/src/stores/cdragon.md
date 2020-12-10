# CDragon

- Type: <Badge text="Pyot Service" vertical="middle" />
- Models: <Badge text="LOL" type="error" vertical="middle" /> <Badge text="TFT" type="error" vertical="middle" />
- Description: Store that provides data from the Community Dragon Raws, this store provides the endpoints for the Pyot Core Objects that returns static data, a list of the endpoints is found below.

:::tip INFO ABOUT THIS STORE
The CDragon has the data that the game uses, but it is highly unparsable, the main goal here is to provide the data as fast as possible unlike the some 3 days delay of DDragon. Since the data structure in CDragon might change at any time without warning, the Pyot Core objects for this might break aswell, submit an issue if this happen and .. will try to fix. It is designed to be fixable in short time in any case UNLESS the jsons goes upside down.
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.CDragon`
### Arguments:
> #### `error_handling: Mapping[int, Tuple[str, List[int]]] = None`
> Define how this store should handle request errors, please refer to [Error Handler](/pipeline/handler.html) documentations at Pipeline.
>
> #### `log_level: int = 10`
> Set the log level for the store. Defaults to 10 (DEBUG level).
>
> #### `version: str = 'latest'`
> Set the version used to make requests. Defaults to `latest`.

:::tip NEW
Starting v1.2.0
- `version` param is added. Now you can set the version used to make requests on the settings.
:::

## Initialization

> ### initialize() <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
>::: danger DEPRECATED
>Removed since v1.1.0, due to adding unnecessary delays on imports.
>:::

## Endpoints

> ### `LOL` <Badge text="Model" type="warning" vertical="middle" />
>`"cdragon_champion_by_id"`
>
>`"cdragon_item_full"`
>
>`"cdragon_rune_full"`
>
>`"cdragon_spells_full"`
>
>`"cdragon_profile_icon_full"`

> ### `TFT` <Badge text="Model" type="warning" vertical="middle" />
>`"cdragon_tft_full"`
>
>`"cdragon_profile_icon_full"`

## Example Usage

```python
{
    "BACKEND": "pyot.stores.CDragon",
    "LOG_LEVEL": 30,
    "VERSION": "pbe",
    "ERROR_HANDLING": {
        404: ("T", []),
        500: ("R", [3])
    }
},
```