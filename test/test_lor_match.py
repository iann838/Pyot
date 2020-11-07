from pyot.utils import loop_run
from pyot.models import lor, riot
from datetime import datetime

async def async_match_history():
    account = await riot.Account(name="Morimorph", tag="na1", region="americas").get(pipeline="lor")
    history = await lor.MatchHistory(puuid=account.puuid, region="americas").get()
    assert isinstance(history.puuid, str)
    for match in history:
        assert isinstance(match, lor.Match)

async def async_match():
    account = await riot.Account(name="Morimorph", tag="na1", region="americas").get(pipeline="lor")
    history = await lor.MatchHistory(puuid=account.puuid, region="americas").get()
    match = await history[0].get()
    info = match.info
    meta = match.metadata
    assert isinstance(meta.data_version, str)
    assert isinstance(meta.match_id, str)
    for puuid in meta.participant_puuids:
        assert isinstance(puuid, str)
    for participant in meta.participants:
        assert isinstance(participant, riot.Account)
    assert isinstance(info.mode, str)
    assert isinstance(info.type, str)
    assert isinstance(info.creation, datetime)
    assert isinstance(info.version, str)
    assert isinstance(info.total_turn_count, int)
    for player in info.players:
        assert isinstance(player.puuid, str)
        assert isinstance(player.deck_id, str)
        assert isinstance(player.deck_code, str)
        for faction in player.factions:
            assert isinstance(faction, str)
        assert isinstance(player.game_outcome, str)
        assert isinstance(player.order_of_play, int)
        assert isinstance(player.win, bool)
        assert isinstance(player.account, riot.Account)
        assert isinstance(player.deck, lor.Deck)


def test_match_history():
    loop_run(async_match_history())

def test_match():
    loop_run(async_match())
