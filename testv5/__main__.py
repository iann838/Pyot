from pyot.models import lol
from pyot.core.queue import Queue
from pyot.utils.sync import async_to_sync


@async_to_sync
async def main():
    summoner = await lol.Summoner(name="Morimorph").get()
    return summoner.dict()


@async_to_sync
async def pull_dev_key_limit():
    challenger = await lol.MasterLeague(queue="RANKED_SOLO_5x5", platform='na1').get()

    summoners = [entry.summoner for entry in challenger.entries[:152]]
    async with Queue() as queue: # type: Queue
        for summoner in summoners:
            await queue.put(summoner.get())
        gotten_summoners = await queue.join(lol.Summoner)
    for i, s in enumerate(gotten_summoners):
        assert s.id == summoners[i].id

    # champion = await lol.Champion(id=777).get()
    # return champion.dict()


@async_to_sync
async def pull_matches():
    summoner = await lol.Summoner(name="Morimorph", platform="na1").get()
    async with Queue() as queue:
        for match in await summoner.match_history.get():
            await queue.put(match.get())
            # break
        return (await queue.join(lol.Match))[-1].dict(recursive=True)


print(pull_matches())
