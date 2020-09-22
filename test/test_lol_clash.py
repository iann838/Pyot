from pyot.utils import loop_run
from pyot.models import lol
from datetime import datetime

# NO ENOUGH SAMPLE TO DO CLASH TEST
# TEST DOESN'T COVER:
    # ClashPlayers (need a summoner that has players entries)
    # ClashTeam (need a team id)
    # ClashTournament (but by team id, same issue)


async def async_tournaments_active():
    clash = await lol.ClashTournaments(platform="NA1").get()
    for tour in clash.tournaments:
        assert isinstance(tour.id, int)
        assert isinstance(tour.theme_id, int)
        assert isinstance(tour.name_key, str)
        assert isinstance(tour.name_key_secondary, str)
        for sched in tour.schedule:
            assert isinstance(sched.id, int)
            assert isinstance(sched.registration_time, datetime)
            assert isinstance(sched.start_time, datetime)
            assert isinstance(sched.cancelled, bool)


async def async_tournament_by_id():
    clash = await lol.ClashTournaments(platform="NA1").get()
    TOURNAMENT_ID = clash.tournaments[0].id
    tour = await lol.ClashTournament(id=TOURNAMENT_ID, platform="NA1").get()
    assert isinstance(tour.id, int)
    assert isinstance(tour.theme_id, int)
    assert isinstance(tour.name_key, str)
    assert isinstance(tour.name_key_secondary, str)
    for sched in tour.schedule:
        assert isinstance(sched.id, int)
        assert isinstance(sched.registration_time, datetime)
        assert isinstance(sched.start_time, datetime)
        assert isinstance(sched.cancelled, bool)


def test_tournaments_active():
    loop_run(async_tournaments_active())

def test_tournament_by_id():
    loop_run(async_tournament_by_id())

