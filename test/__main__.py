import pyot
import asyncio


async def pull_leagues():
    league = await pyot.lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="NA1").get()
    statements = []
    for entry in league.entries[:20]:
        statements.append(entry.summoner.get())
    summoners = await asyncio.gather(*statements)
    for summoner in summoners:
        print(summoner.profile_icon_id)


pyot.run(pull_leagues())