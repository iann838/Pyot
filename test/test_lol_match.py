from datetime import datetime, timedelta
from pyot.utils import loop_run
from pyot.models import lol


def assert_team(team):
    assert isinstance(team.id, int)
    assert isinstance(team.win, bool)
    assert isinstance(team.first_blood, bool)
    assert isinstance(team.first_tower, bool)
    assert isinstance(team.first_inhibitor, bool)
    assert isinstance(team.first_baron, bool)
    assert isinstance(team.first_dragon, bool)
    assert isinstance(team.first_rift_herald, bool)
    assert isinstance(team.tower_kills, int)
    assert isinstance(team.inhibitor_kills, int)
    assert isinstance(team.baron_kills, int)
    assert isinstance(team.dragon_kills, int)
    assert isinstance(team.vilemaw_kills, int)
    assert isinstance(team.rift_herald_kills, int)
    assert isinstance(team.dominion_victory_score, int)
    for ban in team.bans:
        assert isinstance(ban.champion_id, int)
        assert isinstance(ban.pick_turn, int)
        assert isinstance(ban.champion, lol.Champion)
    for p in team.participants:
        assert isinstance(p.id, int)
        assert isinstance(p.team_id, int)
        assert isinstance(p.champion_id, int)
        for spell in p.spell_ids:
            assert isinstance(spell, int)
        for spell2 in p.spells:
            assert isinstance(spell2, lol.Spell)
        stats = p.stats
        assert isinstance(stats.participant_id, int)
        assert isinstance(stats.win, bool)
        assert len(stats.dominion_scores) == 10
        assert len(stats.spell_ids) == 2
        for it in stats.spells:
            assert isinstance(it, lol.Spell)
        assert len(stats.item_ids) == 7
        for it in stats.items:
            assert isinstance(it, lol.Item) or it is None
        assert len(stats.rune_ids) == 6
        for it in stats.runes:
            assert isinstance(it, lol.Rune)
        assert len(stats.stat_rune_ids) == 3
        for it in stats.stat_runes:
            assert isinstance(it, lol.Rune)
        for num in stats.rune_vars:
            assert len(num) == 3
        assert isinstance(stats.rune_main_style, int)
        assert isinstance(stats.rune_sub_style, int)
        assert isinstance(stats.kills, int)
        assert isinstance(stats.deaths, int)
        assert isinstance(stats.assists, int)
        assert isinstance(stats.largest_killing_spree, int)
        assert isinstance(stats.largest_multi_kill, int)
        assert isinstance(stats.killing_sprees, int)
        assert isinstance(stats.longest_time_spent_living, int)
        assert isinstance(stats.double_kills, int)
        assert isinstance(stats.triple_kills, int)
        assert isinstance(stats.quadra_kills, int)
        assert isinstance(stats.penta_kills, int)
        assert isinstance(stats.unreal_kills, int)
        assert isinstance(stats.total_damage_dealt, int)
        assert isinstance(stats.magic_damage_dealt, int)
        assert isinstance(stats.physical_damage_dealt, int)
        assert isinstance(stats.true_damage_dealt, int)
        assert isinstance(stats.largest_critical_strike, int)
        assert isinstance(stats.total_damage_dealt_to_champions, int)
        assert isinstance(stats.magic_damage_dealt_to_champions, int)
        assert isinstance(stats.physical_damage_dealt_to_champions, int)
        assert isinstance(stats.true_damage_dealt_to_champions, int)
        assert isinstance(stats.total_heal, int)
        assert isinstance(stats.total_units_healed, int)
        assert isinstance(stats.damage_self_mitigated, int)
        assert isinstance(stats.damage_dealt_to_objectives, int)
        assert isinstance(stats.damage_dealt_to_turrets, int)
        assert isinstance(stats.vision_score, int)
        assert isinstance(stats.time_ccing_others, int)
        assert isinstance(stats.total_damage_taken, int)
        assert isinstance(stats.magical_damage_taken, int)
        assert isinstance(stats.physical_damage_taken, int)
        assert isinstance(stats.true_damage_taken, int)
        assert isinstance(stats.gold_earned, int)
        assert isinstance(stats.gold_spent, int)
        assert isinstance(stats.turret_kills, int)
        assert isinstance(stats.inhibitor_kills, int)
        assert isinstance(stats.total_minions_killed, int)
        assert isinstance(stats.neutral_minions_killed, int)
        assert isinstance(stats.neutral_minions_killed_team_jungle, int)
        assert isinstance(stats.neutral_minions_killed_enemy_jungle, int)
        assert isinstance(stats.total_time_crowd_control_dealt, int)
        assert isinstance(stats.champ_level, int)
        assert isinstance(stats.vision_wards_bought_in_game, int)
        assert isinstance(stats.sight_wards_bought_in_game, int)
        assert isinstance(stats.wards_placed, int)
        assert isinstance(stats.wards_killed, int)
        assert isinstance(stats.first_blood_kill, bool)
        assert isinstance(stats.first_blood_assist, bool)
        assert isinstance(stats.first_tower_kill, bool)
        assert isinstance(stats.first_tower_assist, bool)
        assert isinstance(stats.first_inhibitor_kill, bool)
        assert isinstance(stats.first_inhibitor_assist, bool)
        assert isinstance(stats.combat_player_score, int)
        assert isinstance(stats.objective_player_score, int)
        assert isinstance(stats.total_player_score, int)
        assert isinstance(stats.total_score_rank, int)
        timeline = p.timeline
        assert isinstance(timeline.participant_id, int)
        assert isinstance(timeline.creeps_per_min_deltas, dict)
        assert isinstance(timeline.xp_per_min_deltas, dict)
        assert isinstance(timeline.gold_per_min_deltas, dict)
        assert isinstance(timeline.cs_diff_per_min_deltas, dict)
        assert isinstance(timeline.xp_diff_per_min_deltas, dict)
        assert isinstance(timeline.damage_taken_per_min_deltas, dict)
        assert isinstance(timeline.damage_taken_diff_per_min_deltas, dict)
        assert isinstance(timeline.role, str)
        assert isinstance(timeline.lane, str)


async def async_match():
    match = await lol.Match(id=3517707030, platform="NA1").get()
    assert isinstance(match.id, int)
    assert isinstance(match.type, str)
    assert isinstance(match.mode, str)
    assert isinstance(match.version, str)
    assert isinstance(match.map_id, int)
    assert isinstance(match.season_id, int)
    assert isinstance(match.queue_id, int)
    assert isinstance(match.creation, datetime)
    assert isinstance(match.duration, timedelta) #not milliseconds
    assert isinstance(match.platform, str)
    for team in match.teams:
        assert_team(team)


async def async_match_timeline():
    match = await lol.Match(id=3517707030, include_timeline=True, platform="NA1").get()
    assert isinstance(match.id, int)
    assert isinstance(match.type, str)
    assert isinstance(match.mode, str)
    assert isinstance(match.version, str)
    assert isinstance(match.map_id, int)
    assert isinstance(match.season_id, int)
    assert isinstance(match.queue_id, int)
    assert isinstance(match.creation, datetime)
    assert isinstance(match.duration, timedelta) #not milliseconds
    assert isinstance(match.platform, str)
    for team in match.teams:
        assert_team(team)
    for team in match.teams:
        for p in team.participants:
            for event in p.timeline.events:
                assert isinstance(event, lol.match.MatchEventData)
            for frame in p.timeline.frames:
                assert isinstance(frame, lol.match.MatchFrameData)
    blue_team2 = match.teams[0] if match.teams[0].id == 100 else match.teams[1]
    red_team2 = match.teams[1] if match.teams[1].id == 200 else match.teams[0]
    for i in range(5):
        assert len(blue_team2.participants[i].timeline.frames) > 30
        assert len(blue_team2.participants[i].timeline.events) > 50
    for i in range(5):
        assert len(red_team2.participants[i].timeline.frames) > 30
        assert len(red_team2.participants[i].timeline.events) > 50


async def async_timeline():
    timeline = await lol.Timeline(id=3517707030, platform="NA1").get()
    assert isinstance(timeline.interval, timedelta)
    assert timeline.interval == timedelta(seconds=60)
    for frame in timeline.frames:
        assert isinstance(frame, lol.match.MatchFrameMinuteData)
        for f in frame.participant_frames:
            assert isinstance(f, lol.match.MatchFrameData)
        for e in frame.events:
            assert isinstance(e, lol.match.MatchEventData)


async def async_match_history():
    summoner = await lol.Summoner(name="Morimorph", platform="NA1").get()
    history = await lol.MatchHistory(account_id=summoner.account_id, platform="NA1").query(begin_index=0, end_index=60, champion_ids=[235]).get()
    assert len(history.matches) == 60
    assert isinstance(history.start_index, int)
    assert isinstance(history.end_index, int)
    assert isinstance(history.total_games, int)
    assert isinstance(history.account_id, str)
    for match in history:
        assert isinstance(match.platform, str)
        assert isinstance(match.id, int)
        assert isinstance(match.champion_id, int)
        assert isinstance(match.queue_id, int)
        assert isinstance(match.season_id, int)
        assert isinstance(match.creation, datetime)
        assert isinstance(match.role, str)
        assert isinstance(match.lane, str)
        assert isinstance(match.match, lol.Match)
        assert isinstance(match.champion, lol.Champion)


def test_match():
    loop_run(async_match())

def test_match_timeline():
    loop_run(async_match_timeline())

def test_timeline():
    loop_run(async_timeline())

def test_match_history():
    loop_run(async_match_history())
