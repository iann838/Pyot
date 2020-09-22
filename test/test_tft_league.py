from pyot.utils import loop_run
from pyot.models import tft
from pyot.core.exceptions import NoContent

LEAGUE_ID = "3e62b5b8-feb0-3089-82e9-675d7ead4374"


def assert_apex_league(league):
    if len(league.entries) == 0:
        return
    assert isinstance(league.tier, str)
    assert isinstance(league.id, str)
    assert isinstance(league.queue, str)
    assert isinstance(league.name, str)
    assert isinstance(league.league, tft.League)
    for entry in league.entries:
        assert isinstance(entry.summoner_id, str)
        assert isinstance(entry.summoner_name, str)
        assert isinstance(entry.league_points, int)
        assert isinstance(entry.rank, str)
        assert isinstance(entry.wins, int)
        assert isinstance(entry.losses, int)
        assert isinstance(entry.veteran, bool)
        assert isinstance(entry.inactive, bool)
        assert isinstance(entry.fresh_blood, bool)
        assert isinstance(entry.hot_streak, bool)
        assert isinstance(entry.summoner, tft.Summoner)


def assert_division_league(entry):
    assert isinstance(entry.summoner_id, str)
    assert isinstance(entry.summoner_name, str)
    assert isinstance(entry.league_points, int)
    assert isinstance(entry.rank, str)
    assert isinstance(entry.wins, int)
    assert isinstance(entry.losses, int)
    assert isinstance(entry.veteran, bool)
    assert isinstance(entry.inactive, bool)
    assert isinstance(entry.fresh_blood, bool)
    assert isinstance(entry.hot_streak, bool)
    assert isinstance(entry.league_id, str)
    assert isinstance(entry.queue, str)
    assert isinstance(entry.tier, str)
    assert isinstance(entry.league, tft.League)
    assert isinstance(entry.summoner, tft.Summoner)
    if hasattr(entry, "mini_series"):
        assert isinstance(entry.mini_series.target, int)
        assert isinstance(entry.mini_series.wins, int)
        assert isinstance(entry.mini_series.losses, int)
        assert isinstance(entry.mini_series.progress, str)


async def async_challenger_league():
    league = await tft.ChallengerLeague(platform="NA1").get()
    assert_apex_league(league)


async def async_grandmaster_league():
    league = await tft.GrandmasterLeague(platform="NA1").get()
    assert_apex_league(league)


async def async_master_league():
    league = await tft.MasterLeague().get()
    assert_apex_league(league)


async def async_division_league_1():
    league = await tft.DivisionLeague(division="III", tier="PLATINUM").query(page=2).get()
    for entry in league.entries:
        assert_division_league(entry)


async def async_division_league_2():
    league = await tft.DivisionLeague(division="III", tier="IRON").get()
    for entry in league.entries:
        assert_division_league(entry)


async def async_summoner_league():
    s = await tft.Summoner(name="Morimorph", platform="NA1").get()
    s_id = s.id
    league = await tft.SummonerLeague(summoner_id=s_id, platform="NA1").get()
    for entry in league.entries:
        assert isinstance(entry.summoner_id, str)
        assert isinstance(entry.summoner_name, str)
        assert isinstance(entry.league_points, int)
        assert isinstance(entry.rank, str)
        assert isinstance(entry.wins, int)
        assert isinstance(entry.losses, int)
        assert isinstance(entry.veteran, bool)
        assert isinstance(entry.inactive, bool)
        assert isinstance(entry.fresh_blood, bool)
        assert isinstance(entry.hot_streak, bool)
        assert isinstance(entry.league_id, str)
        assert isinstance(entry.queue, str)
        assert isinstance(entry.tier, str)


async def async_league():
    league = await tft.League(id=LEAGUE_ID, platform="NA1").get()
    assert isinstance(league.tier, str)
    assert isinstance(league.id, str)
    assert isinstance(league.queue, str)
    assert isinstance(league.name, str)
    for entry in league.entries:
        assert isinstance(entry.summoner_id, str)
        assert isinstance(entry.summoner_name, str)
        assert isinstance(entry.league_points, int)
        assert isinstance(entry.rank, str)
        assert isinstance(entry.wins, int)
        assert isinstance(entry.losses, int)
        assert isinstance(entry.veteran, bool)
        assert isinstance(entry.inactive, bool)
        assert isinstance(entry.fresh_blood, bool)
        assert isinstance(entry.hot_streak, bool)


def test_division_league_1():
    loop_run(async_division_league_1())

def test_division_league_2():
    loop_run(async_division_league_2())

def test_challenger_league():
    loop_run(async_challenger_league())

def test_grandmaster_league():
    loop_run(async_grandmaster_league())

def test_master_league():
    loop_run(async_master_league())

def test_summoner_league():
    loop_run(async_summoner_league())

def test_league():
    loop_run(async_league())
