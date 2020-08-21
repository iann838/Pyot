import datetime
import pyot


async def async_summoner():
    res = await pyot.lol.Summoner(name="Morimorph", platform="NA1").get()
    assert isinstance(res, pyot.lol.Summoner)
    assert isinstance(res.id, str)
    assert isinstance(res.level, int)
    assert isinstance(res.account_id, str)
    assert isinstance(res.puuid, str)
    assert isinstance(res.revision_date, datetime.datetime)
    assert isinstance(res.champion_masteries, pyot.lol.ChampionMasteries)
    assert isinstance(res.league_entries, pyot.lol.SummonerLeague)
    assert isinstance(res.third_party_code, pyot.lol.ThirdPartyCode)


def test_summoner():
    pyot.run(async_summoner())