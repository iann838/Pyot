# Configuration

Pyot requires many setups and configurations in order to work properly.

These configurations generally stays all packed in a single file (generally called `conf.py` or `pyotconf.py`) or one file per model, they must be loaded **once and only once** at application startup.

{% hint style='tip' %}
If an integration of Pyot to another framework is needed. General integration guides are provided for Django, FastAPI and Celery projects at the **Integrations** section. These guides does not require to be strictly followed and only serves for reference purposes.
{% endhint %}

## Models

Module: `pyot.conf.model`

Configurable models: `riot`, `lol`, `tft`, `lor`, `val`

Setup, configure and activate the models of need. Define the default platform, region, version and locale, these are used for default values in class init definitions and object bridging. For a list of correct platforms and regions, they are documented under each models main page.

### _function_ `activate_model` -> `decorator(ModelConf)`
  * Arguments:
    * `name`: Name of model

### _class_ `ModelConf`:
  * Attributes:
    * `default_platform`: `str`
    * `default_region`: `str`
    * `default_version`: `str`
    * `default_locale`: `str`

## Pipelines

Module: `pyot.conf.pipeline`

Configurable models: `lol`, `tft`, `lor`, `val`

Setup, configure and activate a pipeline for the activated models. A pipeline is a list of prioritized data sources that a model will request data from. You may define and activate multiple pipelines under some circumstances, but one and only one default pipeline must exists for each model.

{% hint style='danger' %}
Global models are not configurable as an standalone pipeline, such as `riot`, because objects of multiple other models can access these models objects in their own pipelines. They are configured as part of other models pipelines.
{% endhint %}

### _function_ `activate_pipeline` -> `decorator(PipelineConf)`
  * Arguments:
    * `name`: Name of model this pipeline belongs to

### _class_ `PipelineConf`:
  * Attributes:
    * `name`: `str`
      > Name of this pipeline
    * `default`: `bool`
      > Is this the default pipeline
    * `stores`: `List[Dict[str, Any]]`
      > List of data stores, the earlier the store is located in the list, the higher the priority. Each store has it's own configurations, they are documented in the Stores section.

{% hint style='tip' %}
A variety of stores is provided, including caches (e.g. Redis, MongoDB) and services (e.g. RiotAPI, CDragon). Cache stores must be placed at higher priority than any service stores.

For cache stores, multiple stores of the same backend can be configured, it may be useful for scenarios where different types of objects should be cached in different places (e.g. Two `DiskCache`s with different directory for storing lol matches and lol timelines).
{% endhint %}

## Imports

Conf files can be imported in following ways:

- Using `import_confs` from `pyot.conf.utils`.
- Manually importing the conf file in python syntax.
- If an integration is being used (e.g. Django), check if the integration has a custom conf import hook and use it instead.

### _function_ `import_confs` -> `None`
  * Arguments:
    * `path_or_paths`: Import path or list of import paths to the conf files.

{% hint style='tip' %}
Import path is the path used as if the file/module is being imported using python syntax via `import`, `__import__` or `importlib.import_module`
{% endhint %}

## Example

Example configuration of `lol` model and a default pipeline including a cache store that caches summoners for 100 seconds, matches and timelines for 10 minutes; and service stores for CDragon and RiotAPI:

```python
# myproject/mymodule/pyotconf.py

from pyot.conf.model import activate_model, ModelConf
from pyot.conf.pipeline import activate_pipeline, PipelineConf


@activate_model("lol")
class LolModel(ModelConf):
    default_platform = "na1"
    default_region = "americas"
    default_version = "latest"
    default_locale = "en_us"


@activate_pipeline("lol")
class LolPipeline(PipelineConf):
    name = "lol_main"
    default = True
    stores = [
        {
            "backend": "pyot.stores.omnistone.Omnistone",
            "expirations": {
                "summoner_v4_by_name": 100,
                "match_v4_match": 600,
                "match_v4_timeline": 600,
            }
        },
        {
            "backend": "pyot.stores.cdragon.CDragon",
        },
        {
            "backend": "pyot.stores.riotapi.RiotAPI",
            "api_key": os.environ["RIOT_API_KEY"],
        }
    ]
```

Now import the confs into your application:

```python
# myproject/mymodule/__main__.py

from pyot.conf.utils import import_confs

import_confs("mymodule.pyotconf")
```
