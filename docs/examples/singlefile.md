# Single File

Characteristics:
- Structure: Single File.
- Threading: Single Threaded.

Pros:
- Playground style, easy for testing small features.

Cons:
- Conf and working code mixed together, reducing code readability.
- Some linters may complain about `wrong-import-order`, due to conf must be placed before `from pyot.models import ...`. Can be disabled in linter conf files (e.g. `.pylintrc`)

## Structure

File: `main.py`
```python

import asyncio
import sys
import os
from typing import List

from pyot.core.queue import Queue

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


from pyot.models import lol


async def last_played_champs(summoner_name: str):
    async with Queue() as queue:
        summoner = await lol.Summoner(name=summoner_name).get()
        history = await summoner.match_history.get()
        for match in history.matches[:10]:
            await queue.put(match.get())
        first_10_matches: List[lol.Match] = await queue.join()
    champ_names = []
    for match in first_10_matches:
        for participant in match.info.participants:
            if participant.puuid == summoner.puuid:
                champ_names.append(participant.champion_name)
    return champ_names


if __name__ == "__main__":
    print("Summoner name:", sys.argv[1])
    last_played_champ_names = asyncio.run(last_played_champs(sys.argv[1]))
    print(
        "Last played champ names (last 10 matches):",
        last_played_champ_names,
    )

```


## Run

```
python main.py <summoner_name>
```
