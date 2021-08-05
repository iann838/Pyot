import asyncio
from datetime import datetime
from typing import List, Tuple
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


@async_to_sync
async def pull_timelines_timediff():
    summoner = await lol.Summoner(name="Morimorph", platform="na1").get()
    async with Queue() as queue:
        for timeline in (await summoner.match_history.get()).timelines:
            await queue.put(timeline.get())
            # break
        timelines = await queue.join(lol.Timeline)
    now = datetime.now()
    counter = 0
    for timeline in timelines:
        for frame in timeline.info.frames:
            for _ in frame["events"]:
                counter += 1
    return datetime.now() - now, counter


@async_to_sync
async def pull_league_rate_limiter():
    async with Queue() as queue:
        for i in range(300):
            await queue.put(lol.DivisionLeague(queue="RANKED_SOLO_5x5", division="I", tier="GOLD", platform="na1").query(page=i + 1).get())
    await asyncio.sleep(1)


@async_to_sync
async def pull_match_timelines_inject():
    summoner = await lol.Summoner(name="Morimorph", platform="na1").get()

    async def async_tuple(*coros):
        res = []
        for coro in coros:
            res.append(await coro)
        return tuple(res)

    async with Queue() as queue:
        for match, timeline in (await summoner.match_history.get()).match_timelines:
            await queue.put(async_tuple(match.get(), timeline.get()))
            # break
        match_timelines: List[Tuple[lol.Match, lol.Timeline]] = await queue.join()

    now = datetime.now()
    counter = 0
    for match, timeline in match_timelines:
        match.feed_timeline(timeline)
        for team in match.info.teams:
            for participant in team.participants:
                for _ in participant.events:
                    counter += 1
                print(participant.item_ids)
    return datetime.now() - now, counter


print(pull_match_timelines_inject())
