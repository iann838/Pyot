import pyot
import syot
import asyncio
from typing import List
from datetime import datetime


async def pull_leagues():
    league = await pyot.lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="NA1").get()
    async with pyot.Gatherer() as gatherer: # type: pyot.Gatherer
        gatherer.statements = [entry.summoner for entry in league.entries[:1000]]
        await gatherer.gather()
        responses = gatherer.responses # type: List[pyot.lol.Summoner]
    history = await responses[0].match_history.get()
    match = await history[0].match_timeline.get()
    for team in match.teams:
        for p in team.participants:
            id = p.id
            for frame in p.timeline.frames:
                if frame.participant_id != id:
                    raise Exception
            for event in p.timeline.events:
                try:
                    if event.participant_id != id: raise Exception
                except AttributeError:
                    try:
                        if event.creator_id != id: raise Exception
                    except AttributeError:
                        try:
                            if event.killer_id != id: raise Exception
                        except AttributeError: pass

pyot.run(pull_leagues())
