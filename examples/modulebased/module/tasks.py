
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
