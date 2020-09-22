import datetime
from pyot.utils import loop_run
from pyot.models import lol


async def async_summoner():
    res = await lol.Summoner(name="Morimorph", platform="NA1").get()
    assert isinstance(res, lol.Summoner)
    assert isinstance(res.id, str)
    assert isinstance(res.level, int)
    assert isinstance(res.account_id, str)
    assert isinstance(res.puuid, str)
    assert isinstance(res.revision_date, datetime.datetime)
    assert isinstance(res.champion_masteries, lol.ChampionMasteries)
    assert isinstance(res.league_entries, lol.SummonerLeague)
    assert isinstance(res.third_party_code, lol.ThirdPartyCode)


def test_summoner():
    loop_run(async_summoner())