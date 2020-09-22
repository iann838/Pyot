from pyot.utils import loop_run
from pyot.models import lol
from datetime import datetime, timedelta


async def async_featured_game():
    featured = await lol.FeaturedGames(platform="NA1").get()
    assert isinstance(featured.refresh_interval, timedelta)
    for game in featured.games:
        assert isinstance(game.id, int)
        assert isinstance(game.type, str)
        assert isinstance(game.mode, str)
        assert isinstance(game.creation, datetime)
        assert isinstance(game.duration, timedelta)
        assert isinstance(game.map_id, int)
        assert isinstance(game.platform, str)
        assert isinstance(game.queue, int)
        assert isinstance(game.observers_key, str)
        for team in game.teams:
            assert isinstance(team.id, int)
            for ban in team.bans:
                assert isinstance(ban.pick_turn, int)
                assert isinstance(ban.champion_id, int)
            for p in team.participants:
                assert isinstance(p.champion_id, int)
                assert isinstance(p.profile_icon_id, int)
                assert isinstance(p.is_bot, bool)
                assert isinstance(p.summoner_name, str)
                assert isinstance(p.summoner, lol.Summoner)
                for i in p.spell_ids:
                    assert isinstance(i, int)


async def async_current_game():
    featured = await lol.FeaturedGames(platform="NA1").get()
    s = await featured.games[0].teams[0].participants[0].summoner.get()
    s_id = s.id
    game = await lol.CurrentGame(summoner_id=s_id, platform="NA1").get()
    assert isinstance(game.id, int)
    assert isinstance(game.type, str)
    assert isinstance(game.mode, str)
    assert isinstance(game.creation, datetime)
    assert isinstance(game.duration, timedelta)
    assert isinstance(game.map_id, int)
    assert isinstance(game.platform, str)
    assert isinstance(game.queue, int)
    assert isinstance(game.observers_key, str)
    for team in game.teams:
        assert isinstance(team.id, int)
        for ban in team.bans:
            assert isinstance(ban.pick_turn, int)
            assert isinstance(ban.champion_id, int)
        for p in team.participants:
            assert isinstance(p.champion_id, int)
            assert isinstance(p.profile_icon_id, int)
            assert isinstance(p.is_bot, bool)
            assert isinstance(p.summoner_name, str)
            assert isinstance(p.summoner_id, str)
            assert isinstance(p.rune_style, int)
            assert isinstance(p.rune_sub_style, int)
            for i in p.spell_ids:
                assert isinstance(i, int)
            for i in p.rune_ids:
                assert isinstance(i, int)


def test_featured_games():
    loop_run(async_featured_game())

def test_current_game():
    loop_run(async_current_game())