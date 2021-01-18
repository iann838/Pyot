from pyot.core import Queue
from pyot.models import lol

async def pull_dev_key_limit():
    challenger = await lol.MasterLeague(queue="RANKED_SOLO_5x5").get()
    summoners = [entry.summoner for entry in challenger.entries[:102]]
    async with Queue() as queue: # type: Queue
        for summoner in summoners:
            await queue.put(summoner.get(sid=queue.sid))


async def sync_dev_key_limit():
    challenger = await lol.ChallengerLeague(queue="RANKED_SOLO_5x5").get()
    summoners = [entry.summoner for entry in challenger.entries[:102]]
    for summoner in summoners:
        await summoner.get()
