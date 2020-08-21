import pyot

LEAGUE_ID = "1fd2554b-d9d1-4f09-a5d0-54998d88f516"


def assert_apex_league(league):
    assert isinstance(league.tier, str)
    assert isinstance(league.league_id, str)
    assert isinstance(league.queue, str)
    assert isinstance(league.name, str)
    assert isinstance(league.league, pyot.lol.League)
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
        assert isinstance(entry.summoner, pyot.lol.Summoner)


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
    assert isinstance(entry.league, pyot.lol.League)
    assert isinstance(entry.summoner, pyot.lol.Summoner)
    if hasattr(entry, "mini_series"):
        assert isinstance(entry.mini_series.target, int)
        assert isinstance(entry.mini_series.wins, int)
        assert isinstance(entry.mini_series.losses, int)
        assert isinstance(entry.mini_series.progress, str)


async def async_challenger_league():
    league = await pyot.lol.ChallengerLeague(queue="RANKED_SOLO_5x5", platform="NA1").get()
    assert_apex_league(league)


async def async_grandmaster_league():
    league = await pyot.lol.GrandmasterLeague(queue="RANKED_FLEX_SR", platform="NA1").get()
    assert_apex_league(league)


async def async_master_league():
    league = await pyot.lol.MasterLeague(queue="RANKED_SOLO_5x5").get()
    assert_apex_league(league)


async def async_division_league_1():
    league = await pyot.lol.DivisionLeague(queue="RANKED_SOLO_5x5", division="III", tier="PLATINUM").query(page=2).get()
    for entry in league.entries:
        assert_division_league(entry)


async def async_division_league_2():
    league = await pyot.lol.DivisionLeague(queue="RANKED_FLEX_SR", division="III", tier="IRON").get()
    for entry in league.entries:
        assert_division_league(entry)


async def async_summoner_league():
    s = await pyot.lol.Summoner(name="Morimorph", platform="NA1").get()
    s_id = s.id
    league = await pyot.lol.SummonerLeague(summoner_id=s_id, platform="NA1").get()
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
    league = await pyot.lol.League(id=LEAGUE_ID, platform="NA1").get()
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
    pyot.run(async_division_league_1())

def test_division_league_2():
    pyot.run(async_division_league_2())

def test_challenger_league():
    pyot.run(async_challenger_league())

def test_grandmaster_league():
    pyot.run(async_grandmaster_league())

def test_master_league():
    pyot.run(async_master_league())

def test_summoner_league():
    pyot.run(async_summoner_league())

def test_league():
    pyot.run(async_league())
