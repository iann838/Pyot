import pyot
import syot
import asyncio
from typing import List
from datetime import datetime, timedelta


async def pull_matchlist():
    platforms = ["la1", "la2", "na1"]
    matchlist = set()
    async with pyot.Gatherer(workers=30, cancel_on_raise=True) as gatherer: # type: pyot.Gatherer
        gatherer.statements = []
        gatherer.statements.extend([pyot.lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform=p) for p in platforms])
        gatherer.statements.extend([pyot.lol.GrandmasterLeague(queue="RANKED_SOLO_5x5", platform=p) for p in platforms])
        gatherer.statements.extend([pyot.lol.MasterLeague(queue="RANKED_SOLO_5x5", platform=p) for p in platforms])
        for div in ["I", "II", "III", "IV"]:
            gatherer.statements.extend([pyot.lol.DivisionLeague(queue="RANKED_SOLO_5x5", division=div, tier="DIAMOND", platform=p) for p in platforms])
        await gatherer.gather()
        print(len(gatherer.responses))
        now = datetime.now()
        summoners = []
        for response in gatherer.responses: # type: pyot.lol.ChallengerLeague
            for entry in response.entries:
                summoners.append(entry.summoner)
        gatherer.statements = summoners
        await gatherer.gather()
        print((datetime.now()-now).total_seconds())
        print(len(gatherer.responses))
        begin = round((datetime.now() - timedelta(days=3)).timestamp()*1000)
        gatherer.statements = [response.match_history.query(begin_time=begin) for response in gatherer.responses]
        await gatherer.gather()
        for response in gatherer.responses: # type: pyot.lol.MatchHistory
            for match in response.matches:
                matchlist.add(match.id)
        print(len(matchlist))

pyot.run(pull_matchlist())
