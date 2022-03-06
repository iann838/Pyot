
from pyot.models import lor, riot
from pyot.utils.sync import async_to_sync

from .core import assert_types, assert_walkable


@async_to_sync
async def test_card():
    o = await lor.Cards(set=5, version="latest", locale="en_us").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_ranked():
    o = await lor.Leaderboard(region="americas").get()
    assert_walkable(o)
    assert_types(o)
    o = await lor.Leaderboard(region="sea").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_match():
    a = await riot.Account(game_name="J01", tag_line="KOR").get(pipeline="lor")
    o = await lor.MatchHistory(puuid=a.puuid, region="sea").get()
    assert_walkable(o)
    assert_types(o)
    print(o.ids)
    for ind in range(2):
        o_ = await o[ind].get()
        assert_walkable(o_)
        assert_types(o_)


@async_to_sync
async def test_status():
    o = await lor.Status(region="americas").get()
    assert_walkable(o)
    assert_types(o)
