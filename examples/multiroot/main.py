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
