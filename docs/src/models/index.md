# Models

To import a model:
```python
from pyot.models import val
```

Some model doesn't need a pipeline to work with, but needs a pipeline at run time. For example the `riot` model.

- `RIOT` <Badge text="Model" type="warning" vertical="middle" /> <Badge text="Global" type="error" vertical="middle" />
- `LOL` <Badge text="Model" type="warning" vertical="middle" />
- `TFT` <Badge text="Model" type="warning" vertical="middle" />
- `VAL` <Badge text="Model" type="warning" vertical="middle" />

# Legend

-<Badge text="Model" type="warning" vertical="middle" />: This is a Model

-<Badge text="Global" type="error" vertical="middle" />: This Model **_does not require a pipeline_** to work with, but needs a pipeline at run time.

-<Badge text="Pyot Core" vertical="middle"/>: This object is of type **_Pyot Core_** and can use any of the **_Pyot Core_** API

-<Badge text="Pyot Static" vertical="middle"/>: This object is of type **_Pyot Static_** and can use any of the **_Pyot Static_** API

-<Badge text="param" type="warning" vertical="middle"/>: Available params that can be passed to the Pyot Core object

-<Badge text="pipeline" type="warning" vertical="middle"/>: Provide the pipeline at runtime, receives a string identifying the pipeline (the model e.g. `"val"`)

-<Badge text="query" type="error" vertical="middle"/>: This Pyot Core object can append a query to the token (e.g. a `begin_index` to the LoL `MatchHistory`)

-<Badge text="endpoint" type="error" vertical="middle"/>: The endpoint that the Pyot Core object will use to make external request to gather the data. Typically a legend for manipulating the default expiration maps of Stores of type Cache.

-<Badge text="bridge" type="error" vertical="middle"/>: A "bridge" that returns a instance of another Pyot Core object (e.g. when a `rune_id` is available in the object, there is a high chance that a `rune` bridge is available to return a `Rune` object).

-<Badge text="Iterable" type="warning" vertical="middle"/>: Flags the Pyot Object that it is iterable, meaning it can be indexed or iterated in a loop statement (e.g. `for mastery in champion_masteries: ...` or `champion_masteries[0]` where `champion_masteries` is an instance of `ChampionMasteries`).

-<Badge text="Iterator" type="warning" vertical="middle"/>: The attr of the object that is used as iterator (e.g. in the example above `ChampionMasteries` in _reality_ is iterating through its `masteries` attr which is a list).

