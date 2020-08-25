import pyot
import syot
import asyncio
from typing import List


async def pull_leagues():
    league = await pyot.lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="NA1").get()
    async with pyot.Gatherer() as gatherer: # type: pyot.Gatherer
        gatherer.statements = [entry.summoner for entry in league.entries[:62]]
        await gatherer.gather()
        responses = gatherer.responses # type: List[pyot.lol.Summoner]
    for r in responses:
        await r.profile_icon.get()
    await pyot.lol.Summoner(name="Morimorph", platform="NA1").get()

def pull_leagues_sync():
    league = syot.lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="NA1").get()
    summoners = []
    for entry in league.entries[:10]:
        summoners.append(syot.lol.Summoner(id=entry.summoner_id, platform="NA1").get())
    for r in summoners:
        r.profile_icon_id


pyot.run(pull_leagues())

pull_leagues_sync()