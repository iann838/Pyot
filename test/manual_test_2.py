from typing import List
from datetime import datetime, timedelta
from pyot.models import lol
from pyot.core import Queue, Gatherer, exceptions
from pyot.utils import CloneGenerator, shuffle_list


async def match_history(queue: Queue, matchlist: set, regions: set, summoner: lol.Summoner, begin: timedelta):
    summoner = await summoner.get(sid=queue.sid)
    try:
        history = await summoner.match_history.query(begin_time=begin).get(sid=queue.sid)
        for match in history.matches:
            matchlist.add(match.match_timeline)
            regions.add(match.platform)
    except exceptions.NotFound:
        pass


async def pull_matchlist():
    platforms = ["la1", "na1"]
    matchlist = set()
    regions = set()
    started = datetime.now()
    async with Queue(log_level=30) as queue: # type: Queue
        for p in platforms:
            await queue.put(lol.MasterLeague(queue="RANKED_SOLO_5x5", platform=p).get(sid=queue.sid))
            await queue.put(lol.DivisionLeague(queue="RANKED_SOLO_5x5", division="I", tier="DIAMOND", platform=p).get(sid=queue.sid))
        
        leagues = await queue.join() # type: List[lol.ChallengerLeague]
        _summoners = []
        for league in leagues:
            for entry in league.entries:
                _summoners.append(entry.summoner)
        summoners = CloneGenerator(shuffle_list(_summoners, "platform"))

        begin = round((datetime.now() - timedelta(days=3)).timestamp()*1000)
        for summoner in summoners:
            await queue.put(match_history(queue, matchlist, regions, summoner, begin))
        await queue.join()
    print(len(_summoners))
    print(regions)
    print(datetime.now() - started)