from pyot.utils import loop_run
from pyot.models import val, riot


async def async_leaderboard():
    content = await val.Content(platform="NA").get()
    for act in content.acts:
        if not act.is_active:
            continue
        leaderboard = await act.leaderboard.get()
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


async def async_leaderboard_query():
    content = await val.Content(platform="NA").get()
    for act in content.acts:
        if not act.is_active:
            continue
        leaderboard = await act.leaderboard.query(size=20, start_index=10).get()
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


def test_leaderboard():
    loop_run(async_leaderboard())

def test_leaderboard_query():
    loop_run(async_leaderboard_query())
