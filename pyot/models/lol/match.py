from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Iterator, Dict
import asyncio

from pyot.utils import AutoData, dict_key_value_swap
from pyot.core.functional import turbo_copy, handle_import_error
from .__core__ import PyotCore, PyotStatic

try:
    import roleml
except (ImportError, ValueError):
    pass

try:
    import roleidentification
    champion_roles = AutoData(lambda: defaultdict(lambda: {}, roleidentification.pull_data()))
except ImportError:
    pass


# PYOT STATIC OBJECTS

class MatchPositionData(PyotStatic):
    x: int
    y: int


class MatchBanData(PyotStatic):
    champion_id: int
    pick_turn: int

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id, locale=self.to_locale(self.platform))

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)


class MatchParticipantStatData(PyotStatic):
    participant_id: int
    win: bool
    dominion_scores: List[int]
    spell_ids: List[int]
    item_ids: List[int]
    rune_ids: List[int]
    stat_rune_ids: List[int]
    rune_vars: List[List[int]]
    rune_main_style: int
    rune_sub_style: int
    kills: int
    deaths: int
    assists: int
    largest_killing_spree: int
    largest_multi_kill: int
    killing_sprees: int
    longest_time_spent_living: int
    double_kills: int
    triple_kills: int
    quadra_kills: int
    penta_kills: int
    unreal_kills: int
    total_damage_dealt: int
    magic_damage_dealt: int
    physical_damage_dealt: int
    true_damage_dealt: int
    largest_critical_strike: int
    total_damage_dealt_to_champions: int
    magic_damage_dealt_to_champions: int
    physical_damage_dealt_to_champions: int
    true_damage_dealt_to_champions: int
    total_heal: int
    total_units_healed: int
    damage_self_mitigated: int
    damage_dealt_to_objectives: int
    damage_dealt_to_turrets: int
    vision_score: int
    time_ccing_others: int
    total_damage_taken: int
    magical_damage_taken: int
    physical_damage_taken: int
    true_damage_taken: int
    gold_earned: int
    gold_spent: int
    turret_kills: int
    inhibitor_kills: int
    total_minions_killed: int
    neutral_minions_killed: int
    neutral_minions_killed_team_jungle: int
    neutral_minions_killed_enemy_jungle: int
    total_time_crowd_control_dealt: int
    champ_level: int
    vision_wards_bought_in_game: int
    sight_wards_bought_in_game: int
    wards_placed: int
    wards_killed: int
    first_blood_kill: bool
    first_blood_assist: bool
    first_tower_kill: bool
    first_tower_assist: bool
    first_inhibitor_kill: bool
    first_inhibitor_assist: bool
    combat_player_score: int
    objective_player_score: int
    total_player_score: int
    total_score_rank: int

    class Meta(PyotStatic.Meta):
        raws = ["item_ids", "dominion_scores", "rune_ids", "spell_ids", "rune_vars", "stat_rune_ids"]
        renamed = {"time_c_cing_others": "time_ccing_others", "perk_primary_style": "rune_main_style", "perk_sub_style": "rune_sub_style"}

    @property
    def items(self) -> List["Item"]:
        from .item import Item
        return [Item(id=i, locale=self.to_locale(self.platform)) if i > 0 else None for i in self.item_ids]

    @property
    def meraki_items(self) -> List["MerakiItem"]:
        from .merakiitem import MerakiItem
        return [MerakiItem(id=i) if i > 0 else None for i in self.item_ids]

    @property
    def runes(self) -> List["Rune"]:
        from .rune import Rune
        return [Rune(id=i, locale=self.to_locale(self.platform)) for i in self.rune_ids]

    @property
    def stat_runes(self) -> List["Rune"]:
        from .rune import Rune
        return [Rune(id=i, locale=self.to_locale(self.platform)) for i in self.stat_rune_ids]

    @property
    def spells(self) -> List["Spell"]:
        from .spell import Spell
        return [Spell(id=i, locale=self.to_locale(self.platform)) for i in self.spell_ids]


class MatchFrameData(PyotStatic):
    participant_id: int
    minions_killed: int
    team_score: int
    dominion_score: int
    total_gold: int
    level: int
    xp: int
    current_gold: int
    position: MatchPositionData
    jungle_minions_killed: int


class MatchEventData(PyotStatic):
    lane_type: str
    skill_slot: int
    ascended_type: str
    creator_id: int
    after_id: int
    event_type: str
    type: str
    level_up_type: str
    ward_type: str
    participant_id: int
    tower_type: str
    item_id: int
    before_id: int
    point_captured: str
    monster_type: str
    monster_sub_type: str
    team_id: int
    position: MatchPositionData
    killer_id: int
    timestamp: float
    time: timedelta
    assisting_participant_ids: List[int]
    building_type: str
    victim_id: int

    class Meta(PyotStatic.Meta):
        raws = ["assisting_participant_ids"]

    @property
    def time(self) -> timedelta:
        return timedelta(milliseconds=self.timestamp)

    @property
    def after_item(self) -> "Item":
        from .item import Item
        return Item(id=self.after_id, locale=self.to_locale(self.platform))

    @property
    def item(self) -> "Item":
        from .item import Item
        return Item(id=self.item_id, locale=self.to_locale(self.platform))

    @property
    def before_item(self) -> "Item":
        from .item import Item
        return Item(id=self.before_id, locale=self.to_locale(self.platform))

    @property
    def meraki_after_item(self) -> "MerakiItem":
        from .merakiitem import MerakiItem
        return MerakiItem(id=self.after_id)

    @property
    def meraki_item(self) -> "MerakiItem":
        from .merakiitem import MerakiItem
        return MerakiItem(id=self.item_id)

    @property
    def meraki_before_item(self) -> "MerakiItem":
        from .merakiitem import MerakiItem
        return MerakiItem(id=self.before_id)


class MatchParticipantTimelineData(PyotStatic):
    participant_id: int
    creeps_per_min_deltas: Dict[str, float]
    xp_per_min_deltas: Dict[str, float]
    gold_per_min_deltas: Dict[str, float]
    cs_diff_per_min_deltas: Dict[str, float]
    xp_diff_per_min_deltas: Dict[str, float]
    damage_taken_per_min_deltas: Dict[str, float]
    damage_taken_diff_per_min_deltas: Dict[str, float]
    role: str
    lane: str
    frames: List[MatchFrameData]
    events: List[MatchEventData]

    class Meta(PyotStatic.Meta):
        raws = ["creeps_per_min_deltas", "xp_per_min_deltas", "gold_per_min_deltas", "cs_diff_per_min_deltas",
            "xp_diff_per_min_deltas", "damage_taken_per_min_deltas", "damage_taken_diff_per_min_deltas"]


class MatchParticipantData(PyotStatic):
    id: int
    team_id: int
    champion_id: int
    spell_ids: List[int]
    stats: MatchParticipantStatData
    timeline: MatchParticipantTimelineData
    profile_icon_id: int
    account_id: str
    match_history_uri: str
    current_account_id: str
    current_platform: str
    summoner_name: str
    summoner_id: str
    platform: str

    class Meta(PyotStatic.Meta):
        renamed = {"participant_id": "id", "profile_icon": "profile_icon_id", "platform_id": "platform", "current_platform_id": "current_platform"}
        raws = ["spell_ids"]

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id, locale=self.to_locale(self.platform))

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)

    @property
    def spells(self) -> List["Spell"]:
        from .spell import Spell
        return [Spell(id=i, locale=self.to_locale(self.platform)) for i in self.spell_ids]

    @property
    def account(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(account_id=self.account_id, platform=self.current_platform)

    @property
    def current_account(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(account_id=self.current_account_id, platform=self.current_platform)

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.current_platform)

    @property
    def profile_icon(self) -> "ProfileIcon":
        from .profileicon import ProfileIcon
        return ProfileIcon(id=self.profile_icon_id, locale=self.to_locale(self.current_platform))


class MatchTeamData(PyotStatic):
    id: int
    win: bool
    first_blood: bool
    first_tower: bool
    first_inhibitor: bool
    first_baron: bool
    first_dragon: bool
    first_rift_herald: bool
    tower_kills: int
    inhibitor_kills: int
    baron_kills: int
    dragon_kills: int
    vilemaw_kills: int
    rift_herald_kills: int
    dominion_victory_score: int
    bans: List[MatchBanData]
    participants: List[MatchParticipantData]

    class Meta(PyotStatic.Meta):
        renamed = {"team_id": "id"}


class MatchHistoryData(PyotStatic):
    platform: str
    id: int
    champion_id: int
    queue_id: int
    season_id: int
    timestamp: int
    creation: datetime
    role: str
    lane: str

    class Meta(PyotStatic.Meta):
        renamed = {"platform_id": "platform", "game_id": "id", "champion": "champion_id", "queue": "queue_id", "season": "season_id"}

    @property
    def creation(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp//1000)

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id, locale=self.to_locale(self.platform))

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)

    @property
    def match(self) -> "Match":
        return Match(id=self.id, platform=self.platform)

    @property
    def timeline(self) -> "Timeline":
        return Timeline(id=self.id, platform=self.platform)


class MatchFrameMinuteData(PyotStatic):
    participant_frames: List[MatchFrameData]
    events: List[MatchEventData]
    timestamp: int
    time: timedelta

    @property
    def time(self):
        return timedelta(milliseconds=self.timestamp)


# PYOT CORE OBJECTS

class Match(PyotCore):
    id: int
    type: str
    mode: str
    version: str
    map_id: int
    season_id: int
    queue_id: int
    creation_millis: int
    duration_secs: int
    creation: datetime
    duration: timedelta
    platform: str
    teams: List[MatchTeamData]
    tournament_code: str
    include_timeline: bool

    class Meta(PyotCore.Meta):
        raw_timeline: Dict
        rules = {
            "match_v4_tournament_match": ["tournament_code", "id"],
            "match_v4_match": ["id"],
        }
        renamed = {"game_id": "id", "platform_id": "platform", "game_creation": "creation_millis", "game_duration": "duration_secs",
            "game_version": "version", "game_mode": "mode", "game_type": "type", "queue": "queue_id"}

    def __init__(self, id: int = None, tournament_code: str = None, include_timeline: bool = False, platform: str = None):
        self._lazy_set(locals())

    async def get(self, sid: str = None, pipeline: str = None, deepcopy: bool = False):
        if not self.include_timeline:
            return await super().get(sid, pipeline, deepcopy)
        get_timeline = asyncio.create_task(Timeline(id=self.id, platform=self.platform).get(sid, pipeline, deepcopy))
        get_match = asyncio.create_task(super().get(sid, pipeline, deepcopy))
        await get_match
        timeline = await get_timeline
        self._meta.raw_timeline = timeline.raw()
        self._inject_timeline(timeline.dict())
        return self

    def _turbo_copy(self, data):
        data = data.copy()
        data['teams'] = turbo_copy(data['teams'], 2)
        data['participants'] = turbo_copy(data['participants'], 2)
        for i, p in enumerate(data['participants']):
            data['participants'][i]['stats'] = p['stats'].copy()
            data['participants'][i]['timeline'] = p['timeline'].copy()
        return data

    def _transform(self, data):
        data = self._turbo_copy(data)
        if data["teams"][0]["teamId"] == 100:
            blue_team = data["teams"][0]
            red_team = data["teams"][1]
        else:
            red_team = data["teams"][0]
            blue_team = data["teams"][1]

        blue_team["participants"] = []
        red_team["participants"] = []

        for team in (blue_team, red_team):
            if team["win"] == "Win": team["win"] = True
            else: team["win"] = False

        for p in data["participants"]:
            stats = p["stats"]
            p["spellIds"] = stats["spellIds"] = [p.pop("spell1Id", None), p.pop("spell2Id", None)]

            stats["dominionScores"] = [stats.pop("playerScore"+str(i), None) for i in range(10)]
            stats["itemIds"] = [stats.pop("item"+str(i), None) for i in range(7)]
            stats["runeIds"] = [stats.pop("perk"+str(i), None) for i in range(6)]
            stats["runeVars"] = [[stats.pop("perk"+str(i)+"Var"+str(j), None) for j in range(1, 4)] for i in range(6)]
            stats["statRuneIds"] = [stats.pop("statPerk"+str(i), None) for i in range(3)]

            if p["teamId"] == 100: blue_team["participants"].append(p)
            elif p["teamId"] == 200: red_team["participants"].append(p)

        for pi in data["participantIdentities"]:
            try:
                for platform_key in ("platformId", "currentPlatformId"):
                    if pi["player"][platform_key].lower() == "na":
                        pi["player"][platform_key] = "NA1"
                for team in (blue_team, red_team):
                    for p in team["participants"]:
                        if p["participantId"] == pi["participantId"]:
                            p.update(pi["player"])
            except KeyError: pass

        data.pop("participants"); data.pop("participantIdentities")
        return data

    def _inject_timeline(self, data):
        teams = self._meta.data["teams"]
        frames = {}
        events = {}
        for val in data["frames"][0]["participantFrames"]:
            frames[val["participantId"]] = []
            events[val["participantId"]] = []
        for frame in data["frames"]:
            for val in frame["participantFrames"]:
                frames[val["participantId"]].append(val)
            for event in frame["events"]:
                try: events[event["participantId"]].append(event)
                except KeyError:
                    try: events[event["creatorId"]].append(event)
                    except KeyError:
                        try:
                            events[event["killerId"]].append(event)
                            events[event["victimId"]].append(event)
                        except KeyError:
                            pass
        for key in frames:
            for team in teams:
                found = False
                for participant in team["participants"]:
                    if participant["participantId"] == key:
                        participant["timeline"]["frames"] = frames[key]
                        participant["timeline"]["events"] = events[key]
                        found = True
                        break
                if found: break
        return data

    @handle_import_error("roleml")
    def roleml(self):
        try:
            roles = roleml.predict(self._meta.raw_data, self._meta.raw_timeline)
        except AttributeError as e:
            raise TypeError("This method requires timeline data to execute") from e
        for team in self.teams:
            for participant in team.participants:
                participant.timeline.position = roles[participant.id]
                participant.timeline._meta.data['position'] = roles[participant.id]
        return roles

    @handle_import_error("roleidentification")
    def roleidentification(self):
        resp = {}
        for team in self.teams:
            roles = dict_key_value_swap(roleidentification.get_roles(
                champion_roles.get(),
                [participant.champion_id for participant in team.participants]
            ))
            resp[team.id] = roles
            for participant in team.participants:
                participant.timeline.position = roles[participant.champion_id]
                participant.timeline._meta.data['position'] = roles[participant.champion_id]
        return resp

    def raw_timeline(self):
        return self._meta.raw_timeline

    @property
    def creation(self) -> datetime:
        return datetime.fromtimestamp(self.creation_millis//1000)

    @property
    def duration(self) -> datetime:
        return timedelta(seconds=self.duration_secs)

    @property
    def timeline(self) -> "Timeline":
        return Timeline(id=self.id, platform=self.platform)

    @property
    def blue_team(self) -> MatchTeamData:
        return next(team for team in self.teams if team.id == 100)

    @property
    def red_team(self) -> MatchTeamData:
        return next(team for team in self.teams if team.id == 200)

    @property
    def participants(self) -> List[MatchParticipantData]:
        participants = []
        for team in self.teams:
            participants += team.participants
        return participants


class Timeline(PyotCore):
    frames: List[MatchFrameMinuteData]
    interval_millis: int
    interval: timedelta

    class Meta(PyotCore.Meta):
        rules = {"match_v4_timeline": ["id"]}
        renamed = {"frame_interval": "interval_millis"}

    def __init__(self, id: int = None, platform: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        data = data.copy()
        data["frames"] = data["frames"].copy()
        for i, f in enumerate(data["frames"]):
            data["frames"][i] = f.copy()
            data["frames"][i]["participantFrames"] = list(f["participantFrames"].values())
        return data

    @property
    def interval(self) -> datetime:
        return timedelta(milliseconds=self.interval_millis)


class MatchHistory(PyotCore):
    entries: List[MatchHistoryData]
    start_index: int
    end_index: int
    total_games: int
    account_id: str

    class Meta(PyotCore.Meta):
        allow_query = True
        renamed = {"matches": "entries"}
        rules = {"match_v4_matchlist": ["account_id"]}

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.entries[item]

    def __iter__(self) -> Iterator[MatchHistoryData]:
        return iter(self.entries)

    def __len__(self):
        return len(self.entries)

    def __init__(self, account_id: str = None, platform: str = None):
        self._lazy_set(locals())

    def query(self, champion_ids: List[int] = None, queue_ids: List[int] = None, season_ids: List[int] = None, end_time: int = None, begin_time: int = None, end_index: int = None, begin_index: int = None):
        '''Add query parameters to the object.'''
        kargs = {key if key[-3:] != "ids" else key[:-3] : val for (key, val) in locals().items()}
        for i in [champion_ids, queue_ids, season_ids]:
            if not isinstance(i, list) and i is not None:
                raise RuntimeError("Query parameters 'champion_ids', 'queue_ids' and 'season_ids' must be a list of values")
        self._meta.query = self._parse_camel(kargs)
        return self

    @property
    def matches(self) -> List[Match]:
        return [Match(id=entry.id, platform=entry.platform) for entry in self.entries]

    @property
    def match_timelines(self) -> List[Match]:
        return [Match(id=entry.id, include_timeline=True, platform=entry.platform) for entry in self.entries]

    @property
    def timelines(self) -> List[Timeline]:
        return [Timeline(id=entry.id, platform=entry.platform) for entry in self.entries]

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(account_id=self.account_id, platform=self.platform)


class Matches(PyotCore):
    ids: List[int]
    tournament_code: str

    class Meta(PyotCore.Meta):
        rules = {"match_v4_tournament_matches": ["tournament_code"]}
        raws = ["ids"]

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.ids[item]

    def __iter__(self) -> Iterator[int]:
        return iter(self.ids)

    def __len__(self):
        return len(self.ids)

    def __init__(self, tournament_code: str = None, platform: str = None):
        self._lazy_set(locals())

    @property
    def matches(self) -> List[Match]:
        return [Match(id=id_, tournament_code=self.tournament_code, platform=self.platform) for id_ in self.ids]

    @property
    def match_timelines(self) -> List[Match]:
        return [Match(id=id_, tournament_code=self.tournament_code, include_timeline=True, platform=self.platform) for id_ in self.ids]

    @property
    def timelines(self) -> List[Timeline]:
        return [Timeline(id=id_, platform=self.platform) for id_ in self.ids]

    def _transform(self, data):
        return {"ids": data}
