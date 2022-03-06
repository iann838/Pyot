
from pyot.models import val
from pyot.utils.sync import async_to_sync

from .core import assert_types, assert_walkable


@async_to_sync
async def test_content():
    o = await val.Content().query(locale="en-US").get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_ranked():
    c = await val.Content().get()
    latest_act = next(act for act in reversed(c.acts) if act.is_active and act.type == 'act')
    act_id = latest_act.id
    o = await val.Leaderboard(act_id=act_id, platform="eu").get()
    assert_walkable(o)
    assert_types(o)
    o = await val.Leaderboard(act_id=act_id, platform="eu").query(size=200, start_index=220).get()
    assert_walkable(o)
    assert_types(o)


@async_to_sync
async def test_match():
    c = await val.Content().get()
    latest_act = next(act for act in reversed(c.acts) if act.is_active and act.type == 'act')
    act_id = latest_act.id
    l = await val.Leaderboard(act_id=act_id, platform="eu").get()
    o = await val.MatchHistory(puuid=l[0].puuid, platform="eu").get()
    assert_walkable(o)
    assert_types(o)
    for ind in range(2):
        o_ = await o[ind].get()
        assert_walkable(o_)
        assert_types(o_)


@async_to_sync
async def test_status():
    o = await val.Status(platform="eu").get()
    assert_walkable(o)
    assert_types(o)
