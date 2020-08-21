import pyot
from datetime import datetime


async def async_champion_masteries():
    s = await pyot.lol.Summoner(name="Morimorph").get()
    s_id = s.id
    res = await pyot.lol.ChampionMasteries(summoner_id=s_id, platform="NA1").get()
    assert isinstance(res.summoner_id, str)
    assert isinstance(res.summoner, pyot.lol.Summoner)
    assert isinstance(res.platform, str)
    assert isinstance(res.masteries, list)
    for mastery in res.masteries:
        assert isinstance(mastery.champion_id, int)
        assert isinstance(mastery.champion_level, int)
        assert isinstance(mastery.champion_points, int)
        assert isinstance(mastery.last_play_time, datetime)
        assert isinstance(mastery.champion_points_since_last_level, int)
        assert isinstance(mastery.champion_points_until_next_level, int)
        assert isinstance(mastery.chest_granted, bool)
        assert isinstance(mastery.tokens_earned, int)
        assert isinstance(mastery.summoner_id, str)
        assert isinstance(res.summoner, pyot.lol.Summoner)


async def async_champion_mastery():
    s = await pyot.lol.Summoner(name="Morimorph").get()
    s_id = s.id
    res = await pyot.lol.ChampionMastery(summoner_id=s_id, platform="NA1", champion_id=235).get()
    assert isinstance(res.champion_id, int)
    assert isinstance(res.champion_level, int)
    assert isinstance(res.champion_points, int)
    assert isinstance(res.last_play_time, datetime)
    assert isinstance(res.champion_points_since_last_level, int)
    assert isinstance(res.champion_points_until_next_level, int)
    assert isinstance(res.chest_granted, bool)
    assert isinstance(res.tokens_earned, int)
    assert isinstance(res.summoner_id, str)
    assert isinstance(res.summoner, pyot.lol.Summoner)


def test_champion_masteries():
    pyot.run(async_champion_masteries())

def test_champion_mastery():
    pyot.run(async_champion_mastery())