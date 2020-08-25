import pyot
import asyncio
from typing import List


async def pull_leagues():
    league = await pyot.lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="NA1").get()
    async with pyot.Gatherer() as gatherer: # type: pyot.Gatherer
        gatherer.statements = [entry.summoner for entry in league.entries[:62]]
        await gatherer.gather()
        responses = gatherer.responses # type: List[pyot.lol.Summoner]
    for r in responses:
        r.profile_icon_id


pyot.run(pull_leagues())