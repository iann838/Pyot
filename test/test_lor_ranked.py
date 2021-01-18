from pyot.utils import loop_run
from pyot.models import lor


async def async_leaderboard():
    leaderboard = await lor.Leaderboard(region="Americas").get()
    for player in leaderboard:
        assert isinstance(player.name, str)
        assert isinstance(player.rank, int)
        assert isinstance(player.lp, int) or isinstance(player.lp, float)


def test_leaderboard():
    loop_run(async_leaderboard())
