from pyot.utils import loop_run
from pyot.core.exceptions import NotFound
from pyot.models import val, riot


async def async_leaderboard():
    successed = 0
    content = await val.Content(platform="NA").get()
    for act in content.acts:
        if not act.is_active:
            continue
        try:
            leaderboard = await act.leaderboard.get()
            successed += 1
        except NotFound as e:
            pass
        assert isinstance(leaderboard.act_id, str)
        assert isinstance(leaderboard.total_players, int)
        assert isinstance(leaderboard.shard, str)
        for player in leaderboard:
            assert isinstance(player.puuid, str)
            assert isinstance(player.game_name, str)
            assert isinstance(player.tag_line, str)
            assert isinstance(player.leaderboard_rank, int)
            assert isinstance(player.ranked_rating, int)
            assert isinstance(player.number_of_wins, int)
            assert isinstance(player.account, riot.Account)
    assert successed > 0


async def async_leaderboard_query():
    successed = 0
    content = await val.Content(platform="NA").get()
    for act in content.acts:
        if not act.is_active:
            continue
        try:
            leaderboard = await act.leaderboard.query(size=20, start_index=10).get()
            successed += 1
        except NotFound as e:
            pass
        assert isinstance(leaderboard.act_id, str)
        assert isinstance(leaderboard.total_players, int)
        assert isinstance(leaderboard.shard, str)
        for player in leaderboard.players:
            assert isinstance(player.puuid, str)
            assert isinstance(player.game_name, str)
            assert isinstance(player.tag_line, str)
            assert isinstance(player.leaderboard_rank, int)
            assert isinstance(player.ranked_rating, int)
            assert isinstance(player.number_of_wins, int)
            assert isinstance(player.account, riot.Account)
    assert successed > 0


def test_leaderboard():
    loop_run(async_leaderboard())

def test_leaderboard_query():
    loop_run(async_leaderboard_query())
