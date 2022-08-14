# Module Based

Characteristics:
- Structure: Module based.
- Threading: Single Threaded.

Pros:
- Better code structure for higher maintainability.
- Conf imports is handled by `__init__.py` only for cleaner imports.
- Although not used in this example, using `__main__.py` may be more elegant in some situations.

Cons:
- No significant cons.

## Structure

File: `module/__init__.py`
```python

from pyot.conf.utils import import_confs

import_confs("module.pyotconf")

```

File: `module/pyotconf.py`
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

File: `module/tasks.py`
```python

from typing import List
import statistics

from pyot.core.queue import Queue
from pyot.models import lol


async def average_win_rate_10_matches(summoner_name: str):
    async with Queue() as queue:
        summoner = await lol.Summoner(name=summoner_name).get()
        history = await summoner.match_history.get()
        for match in history.matches[:10]:
            await queue.put(match.get())
        first_10_matches: List[lol.Match] = await queue.join()
    wins = []
    for match in first_10_matches:
        for participant in match.info.participants:
            if participant.puuid == summoner.puuid:
                wins.append(int(participant.win))
    return statistics.mean(wins or [0])

```

File: `main.py`
```python
import asyncio
import sys

from module.tasks import average_win_rate_10_matches


if __name__ == "__main__":
    print("Summoner name:", sys.argv[1])
    average_win_rate = asyncio.run(average_win_rate_10_matches(sys.argv[1]))
    print(
        "Average win rate (last 10 matches):",
        average_win_rate * 100, "%"
    )

```


## Run

```
python main.py <summoner_name>
```
