# Multi Root

Characteristics:
- Structure: Multi Root.
- Threading: Single Threaded.

Pros:
- Playground style, easy for testing small features.
- Conf and working code are in separate files.

Cons:
- Some linters may complain about `wrong-import-order`, due to conf must be placed before `from pyot.models import ...`. Can be disabled in linter conf files (e.g. `.pylintrc`) or use python syntax `import ...` instead of `import_confs(...)` but that will cause linters to complain `unused-import`.

## Structure

File: `main.py`
```python
import asyncio
import sys
from typing import List
import statistics

from pyot.conf.utils import import_confs
import_confs("pyotconf")
from pyot.core.queue import Queue
from pyot.models import lol


async def average_match_duration_millis(summoner_name: str):
    async with Queue() as queue:
        summoner = await lol.Summoner(name=summoner_name).get()
        history = await summoner.match_history.get()
        for match in history.matches[:10]:
            await queue.put(match.get())
        first_10_matches: List[lol.Match] = await queue.join()
    return statistics.mean([match.info.duration_millis for match in first_10_matches] or [0])


if __name__ == "__main__":
    print("Summoner name:", sys.argv[1])
    avr_match_duration_millis = asyncio.run(average_match_duration_millis(sys.argv[1]))
    print(
        "Average match duration (last 10 matches):",
        avr_match_duration_millis,
        "milliseconds", "(~",
        avr_match_duration_millis / 1000 / 60, "minutes)"
    )

```

File: `pyotconf.py`
```python

import os
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


## Run

```
python main.py <summoner_name>
```
