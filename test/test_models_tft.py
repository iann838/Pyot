from pyot.models import tft
from pyot.utils.sync import async_to_sync
from pyot.utils.tft.routing import platform_to_region

from .core import assert_types, assert_walkable


@async_to_sync
async def test_champion():
    o = await tft.Champions(version="pbe", locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await tft.Champion(key=o[0].key, locale="es_mx").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_item():
    o = await tft.Items(version="pbe", locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await tft.Item(id=o[0].id, version="pbe", locale="es_mx").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_league():
    o = await tft.ChallengerLeague(platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await tft.GrandmasterLeague(platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await tft.MasterLeague(platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await tft.League(id=o.id, platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    s = await tft.Summoner(name="Morimorph", platform="na1").get()
    o = await tft.SummonerLeague(summoner_id=s.id, platform="na1").get()
    assert_walkable(o)
    assert_types(o)
    o = await tft.DivisionLeague(tier="GOLD", division="I", platform="na1").query(page=1).get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_match():
    s = await tft.Summoner(name="Morimorph", platform="na1").get()
    o = await tft.MatchHistory(puuid=s.puuid, region=platform_to_region(s.platform)).query(count=100).get()
    assert_walkable(o)
    assert_types(o)
    o = await s.match_history.query(count=100).get()
    assert_walkable(o)
    assert_types(o)
    for ind in range(2):
        i = o[ind].id
        o_ = await o[ind].get()
        assert_walkable(o_)
        assert_types(o_)
        o1 = await tft.Match(id=i, region=platform_to_region(s.platform)).get()
        assert_walkable(o1)
        assert_types(o1)


@async_to_sync
async def test_profileicon():
    o = await tft.ProfileIcons(locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await o[230].get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_summoner():
    o = await tft.Summoner(name="Morimorph").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_trait():
    o = await tft.Traits(version="pbe", locale="en_us").get()
    assert_walkable(o)
    assert_types(o)
    o = await tft.Trait(key=o[0].key, version="pbe", locale="es_mx").get()
    assert_walkable(o)
    assert_types(o)
