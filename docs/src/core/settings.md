# Settings

::: warning
First words: Pyot WON'T work if you don't activate the settings for the respective models (games).
:::

Pyot Settings are passed as constructors parameters to the class. It takes the necessary objects to change how Pyot behave to your needs. Each model (game) should have their own settings and therefore their own pipeline declared in the settings.

:::tip REMINDER
Don't forget to call `activate()` at the end of your settings instantiation.
:::

## Pyot Settings API

This object is imported ~~at Pyot's root level as `Settings`~~(Removed since v1.1.0) at the core module.
```python{1}
from pyot.core import Settings

Settings(
    # settings params ...
).activate() # activate
```

Pyot Settings should be **_activated_** on your main module's `__init__.py` or before your script `main()` entry point.
```python
├─ foo
│  ├─ __init__.py  # <---- HERE MOSTLY
│  ├─ __main__.py  # <---- OR ANYWHERE BEFORE CALLING `main()`
│  └─ bar.py
# ...
```

> ### `__init__(**kwargs)`
> Create an instance of the Pyot Object, See parameters:
> - `MODEL` <Badge text="param" type="warning" vertical="middle"/> -> `str`: The name of the model, a valid 3 letter model name is passed (`"LOL"`, `"VAL"`, `"TFT"`, `"RIOT"`, soontm `"LOR"`)
>
> - `DEFAULT_PLATFORM` <Badge text="param" type="warning" vertical="middle"/> -> `str`: Default platform to use when no platform is passed to Pyot Core Objects, platform values varies from model, refer to each model at API section.
>
> - `DEFAULT_REGION` <Badge text="param" type="warning" vertical="middle"/> -> `str`: Default region to use when no region is passed to Pyot Core Objects, region values varies from model, refer to each model at API section.
>
> - `DEFAULT_LOCALE` <Badge text="param" type="warning" vertical="middle"/> -> `str`: Default locale to use when no locale is passed to Pyot Core Objects, locale values varies from model, refer to each model at API section.
>
> - `LOCALE_MAP` <Badge text="param" type="warning" vertical="middle"/> -> `Mapping[str, str]`: A dictionary that contains the key value pairs to override the default mapping to locale, this mapping is used for converting platform and regions to locale when "bridges" are called, for example, calling a bridge that brings a `Champion` instance from a `ChampionMastery` instance with platform `"KR"` will bring `Champion` with locale `ko_kr` by default, you can override the region/platform/locale on runtime too, simply `x.locale = "en_us"` where x is a locale based Core Object. For values refer to each model at API section
> :::tip INFO
> Since v1.0.7 you can use the wildcard key (`"*"`) to identify "remaining" locales.
> :::
>
> - `GATHERER` <Badge text="param" type="warning" vertical="middle"/> -> `Mapping[str, Any]`: Gatherer original argument
> ::: danger DEPRECATED
> Removed since v1.1.0.
> :::
>
> - `PIPELINE` <Badge text="param" type="warning" vertical="middle"/> -> `List[Mapping[str, Any]]`: A list of dict of stores that defines the Pipeline used for the model. **_For each item in the list, DEFINE the `BACKEND` of the Store plus other required or optional settings, these settings are documented in a per Store basic_**. Please refer to Pipeline section for more details and Stores section for its settings params and available stores for each model.

> ### `activate()` <Badge text="function" type="error" vertical="middle"/>
> Activates the Settings object by creating the needed pipeline and adjusting the Gatherer and defaults.

## Example Usage
:::tip
Each Pipeline Store can receive different params, check out the PipelineStores tab for more info.
The Gatherer info is in the next section.
:::
```python
from pyot.core import Settings
import os

Settings(
    MODEL = "LOL",
    DEFAULT_PLATFORM = "NA1",
    DEFAULT_REGION = "AMERICAS",
    DEFAULT_LOCALE= "EN_US",
    PIPELINE = [
        {
            "BACKEND": "pyot.stores.Omnistone",
        },
        {
            "BACKEND": "pyot.stores.MerakiCDN",
            "ERROR_HANDLING": {
                500: ("E", [2, 3])
            }
        },
        {
            "BACKEND": "pyot.stores.CDragon",
            "ERROR_HANDLING": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "BACKEND": "pyot.stores.RiotAPI",
            "API_KEY": os.environ["RIOT_API_KEY"],
            "LOG_LEVEL": 30,  # <-- 30 to put at warning level so python prints it.
            "RATE_LIMITER": {
                "BACKEND": "pyot.limiters.MemoryLimiter",
                "LIMITING_SHARE": 1,
            },
            "ERROR_HANDLING": {
                400: ("T", []),
                503: ("E", [3, 3])
            }
        }
    ]
).activate()
```