from pyot.utils import loop_run
from pyot.models import val, riot
from datetime import datetime, timedelta

async def async_match_history():
    account = await riot.Account(name="stelar7", tag="stl7", region="AMERICAS").get(pipeline="val")
    history = await val.MatchHistory(puuid=account.puuid, platform="eu").get()
    for match in history:
        assert isinstance(match, val.Match)
        assert isinstance(match.id, str)
        assert isinstance(match.creation, datetime)
        assert isinstance(match.team_id, str)


async def async_match():
    account = await riot.Account(name="stelar7", tag="stl7", region="AMERICAS").get(pipeline="val")
    history = await val.MatchHistory(puuid=account.puuid, platform="eu").get()
    match = await history[0].get()
    info = match.info
    players = match.players
    teams = match.teams
    results = match.round_results
    assert isinstance(info.id, str)
    assert isinstance(info.map_id, str)
    assert isinstance(info.duration, timedelta)
    assert isinstance(info.creation, datetime)
    assert isinstance(info.provisioning_flow_id, str)
    assert isinstance(info.is_completed, bool)
    assert isinstance(info.custom_game_name, str)
    assert isinstance(info.queue_id, str)
    assert isinstance(info.game_mode, str)
    assert isinstance(info.is_ranked, bool)
    assert isinstance(info.season_id, str)
    for i in players:
        assert isinstance(i.puuid, str)
        assert isinstance(i.team_id, str)
        assert isinstance(i.party_id, str)
        assert isinstance(i.character_id, str)
        assert isinstance(i.competitive_tier, int)
        assert isinstance(i.player_card, str)
        assert isinstance(i.player_title, str)
        stat = i.stats
        assert isinstance(stat.score, int)
        assert isinstance(stat.rounds_played, int)
        assert isinstance(stat.kills, int)
        assert isinstance(stat.deaths, int)
        assert isinstance(stat.assists, int)
        assert isinstance(stat.playtime, timedelta)
        ability = stat.ability_casts
        if ability is not None:
            assert isinstance(ability.grenade_casts, int) if ability.grenade_casts is not None else True 
            assert isinstance(ability.ability1_casts, int) if ability.ability1_casts is not None else True 
            assert isinstance(ability.ability2_casts, int) if ability.ability2_casts is not None else True 
            assert isinstance(ability.ultimate_casts, int) if ability.ultimate_casts is not None else True 
    for i in teams:
        assert isinstance(i.id, str)
        assert isinstance(i.won, bool)
        assert isinstance(i.rounds_played, int)
        assert isinstance(i.rounds_won, int)
    for i in results:
        assert isinstance(i.round_num, int)
        assert isinstance(i.round_result, str)
        assert isinstance(i.round_ceremony, str)
        assert isinstance(i.winning_team, str)
        # assert isinstance(i.bomb_planter_puuid, str)
        # assert isinstance(i.bomb_defuser_puuid, str)
        assert isinstance(i.plant_round_time, timedelta)
        assert isinstance(i.plant_site, str)
        assert isinstance(i.defuse_round_time, timedelta)
        assert isinstance(i.round_result_code, str)
        l1 = i.defuse_location
        l2 = i.plant_location
        assert isinstance(l1.x, int)
        assert isinstance(l1.y, int)
        assert isinstance(l2.x, int)
        assert isinstance(l2.y, int)
        defuse = i.defuse_player_locations
        plant = i.plant_player_locations
        for pi in [defuse, plant]:
            if pi is not None:
                for p in pi:
                    assert isinstance(p.puuid, str)
                    assert isinstance(p.view_radians, float)
                    assert isinstance(p.location.x, int)
                    assert isinstance(p.location.y, int)
        pss = i.player_stats
        for ps in pss:
            assert isinstance(ps.puuid, str)
            assert isinstance(ps.score, int)
            for k in ps.kills:
                assert isinstance(k.game_duration, timedelta)
                assert isinstance(k.round_duration, timedelta)
                assert isinstance(k.killer_puuid, str)
                assert isinstance(k.victim_puuid, str)
                assert k.assistant_puuids is not None
                assert isinstance(k.victim_location.x, int)
                assert isinstance(k.victim_location.y, int)
                for pl in k.player_locations:
                    assert isinstance(pl.puuid, str)
                    assert isinstance(pl.view_radians, float) or pl.view_radians == 0
                    assert isinstance(pl.location.x, int)
                    assert isinstance(pl.location.y, int)
                fd = k.finishing_damage
                assert isinstance(fd.damage_type, str)
                assert isinstance(fd.damage_item, str)
                assert isinstance(fd.is_secondary_fire_mode, bool)
            for d in ps.damage:
                assert isinstance(d.receiver, str)
                assert isinstance(d.damage, int)
                assert isinstance(d.legshots, int)
                assert isinstance(d.bodyshots, int)
                assert isinstance(d.headshots, int)
            ec = ps.economy
            assert isinstance(ec.loadout_value, int)
            assert isinstance(ec.weapon, str)
            assert isinstance(ec.armor, str)
            assert isinstance(ec.remaining, int)
            assert isinstance(ec.spent, int)
            abi = ps.ability
            assert isinstance(abi.grenade_effects, int) if abi.grenade_effects is not None else True
            assert isinstance(abi.ability1_effects, int) if abi.ability1_effects is not None else True
            assert isinstance(abi.ability2_effects, int) if abi.ability2_effects is not None else True
            assert isinstance(abi.ultimate_effects, int) if abi.ultimate_effects is not None else True


async def async_recent():
    recent = await val.RecentMatches(queue="competitive", platform="NA").get()
    assert isinstance(recent.current_time, datetime)
    for match in recent.matches:
        assert isinstance(match, val.Match)
        assert match.platform == recent.platform


def test_match_history():
    loop_run(async_match_history())

def test_match():
    loop_run(async_match())

def test_recent():
    loop_run(async_recent())
