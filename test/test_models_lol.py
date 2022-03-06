from datetime import datetime, timedelta

from pyot.models import lol
from pyot.utils.sync import async_to_sync
from pyot.utils.lol.routing import platform_to_region

from .core import assert_types, assert_walkable


@async_to_sync
async def test_champion():
    o = await lol.Champion(id=81, locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.Champion(key="Irelia", locale="es_mx", version="12.1").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.Champions(version="pbe").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_championmastery():
    s = await lol.Summoner(name="Morimorph", platform="na1").get()
    o = await lol.ChampionMasteries(summoner_id=s.id, platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.ChampionMastery(summoner_id=s.id, champion_id=39, platform="na1").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_championrotation():
    o = await lol.ChampionRotation(platform="na1").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_clash():
    o = await lol.ClashTournaments(platform="na1").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_item():
    o = await lol.Item(id=2003, locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.Items(locale="en_us").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_league():
    o = await lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.GrandmasterLeague(queue="RANKED_SOLO_5x5", platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.MasterLeague(queue="RANKED_SOLO_5x5", platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.League(id=o.id, platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    s = await lol.Summoner(name="Morimorph", platform="na1").get()
    o = await lol.SummonerLeague(summoner_id=s.id, platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.DivisionLeague(tier="GOLD", division="I", queue="RANKED_SOLO_5x5", platform="na1").query(page=1).get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_match():
    s = await lol.Summoner(name="Morimorph", platform="na1").get()
    o = await lol.MatchHistory(puuid=s.puuid, region=platform_to_region(s.platform)).query(count=100, queue=420).get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.MatchHistory(puuid=s.puuid, region=platform_to_region(s.platform)).query(count=100, queue=420, start_time=int((datetime.now() - timedelta(days=200)).timestamp())).get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.MatchHistory(puuid=s.puuid, region=platform_to_region(s.platform)).query(count=100, queue=420, start_time=datetime.now() - timedelta(days=200)).get()
    assert_walkable(o)
    assert_types(o)
    o = await s.match_history.query(count=100, queue=420, start_time=datetime.now() - timedelta(days=200)).get()
    assert_walkable(o)
    assert_types(o)
    for ind in range(2):
        i = o[ind].id
        o_ = await o[ind].get()
        assert_walkable(o_)
        assert_types(o_)
        o1 = await lol.Match(id=i, region=platform_to_region(s.platform)).get()
        assert_walkable(o1)
        assert_types(o1)
        o2 = await lol.Timeline(id=i, region=platform_to_region(s.platform)).get()
        assert_walkable(o2)
        assert_types(o2)
        o1.feed_timeline(o2)
        assert_walkable(o1)
        assert_types(o1)


@async_to_sync
async def test_merakichampion():
    o = await lol.MerakiChampion(id=39).get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.MerakiChampion(key="Irelia").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.MerakiChampion(name="Irelia").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_merakiitem():
    o = await lol.MerakiItem(id=2003).get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_profileicon():
    o = await lol.ProfileIcons(locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await o[230].get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_rune():
    o = await lol.Runes(locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.Rune(id=o[12].id, locale="en_us").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_spectator():
    o = await lol.FeaturedGames(platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    s = await o[0].participants[0].summoner.get()
    o = await lol.CurrentGame(summoner_id=s.id, platform=s.platform).get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_spell():
    o = await lol.Spells(locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await lol.Spell(id=12, locale="en_us", version="pbe").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_status():
    o = await lol.Status(platform="na1").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_summoner():
    o = await lol.Summoner(name="Morimorph").get()
    assert_walkable(o)
    assert_types(o)
