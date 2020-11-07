from pyot.utils import loop_run
from pyot.models import tft
from datetime import datetime, timedelta

async def async_match_history():
    summoner = await tft.Summoner(name="Morimorph", platform="na1").get()
    history = await summoner.match_history.get()
    assert isinstance(history.puuid, str)
    for i in history:
        assert isinstance(i, tft.Match)

async def async_match():
    summoner = await tft.Summoner(name="Morimorph", platform="na1").get()
    history = await summoner.match_history.get()
    match = await history[0].get()
    info = match.info
    assert isinstance(info.creation, datetime)
    assert isinstance(info.duration, timedelta)
    assert isinstance(info.variation, str)
    assert isinstance(info.version, str)
    assert isinstance(info.queue_id, int)
    assert isinstance(info.tft_set_number, int)
    for p in info.participants:
        assert isinstance(p.gold_left, int)
        assert isinstance(p.last_round, int)
        assert isinstance(p.level, int)
        assert isinstance(p.placement, int)
        assert isinstance(p.players_eliminated, int)
        assert isinstance(p.puuid, str)
        assert isinstance(p.time_eliminated, timedelta)
        assert isinstance(p.total_damage_to_players, int)
        companion = p.companion
        assert isinstance(companion.content_id, str)
        assert isinstance(companion.skin_id, int)
        assert isinstance(companion.species, str)
        for t in p.traits:
            assert isinstance(t.name, str)
            assert isinstance(t.num_units, int)
            assert isinstance(t.style, int)
            assert isinstance(t.tier_current, int)
            assert isinstance(t.tier_total, int)
        for u in p.units:
            assert isinstance(u.item_ids, list)
            assert isinstance(u.champion_key, str)
            assert isinstance(u.name, str)
            assert isinstance(u.rarity, int)
            assert isinstance(u.tier, int)
    metadata = match.metadata
    assert isinstance(metadata.id, str)
    assert isinstance(metadata.data_version, str)
    assert isinstance(metadata.participant_puuids, list)


def test_match_history():
    loop_run(async_match_history())

def test_match():
    loop_run(async_match())