from datetime import datetime, timedelta
import re
from typing import List, Iterator, Dict, TYPE_CHECKING, Tuple, Union

from pyot.conf.model import models
from pyot.core.functional import parse_camelcase, lazy_property

from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from .item import Item
    from .champion import Champion
    from .merakichampion import MerakiChampion
    from .merakiitem import MerakiItem
    from .rune import Rune
    from .spell import Spell
    from .summoner import Summoner


# PYOT STATIC OBJECTS

class MatchBanData(PyotStatic):
    champion_id: int
    pick_turn: int

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id)

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)


class MatchObjectiveDetailData(PyotStatic):
    first: bool
    kills: int


class MatchObjectiveData(PyotStatic):
    baron: MatchObjectiveDetailData
    champion: MatchObjectiveDetailData
    dragon: MatchObjectiveDetailData
    inhibitor: MatchObjectiveDetailData
    rift_herald: MatchObjectiveDetailData
    tower: MatchObjectiveDetailData


class MatchTeamData(PyotStatic):
    id: int
    win: bool
    bans: List[MatchBanData]
    objectives: MatchObjectiveData

    class Meta(PyotStatic.Meta):
        renamed = {"team_id": "id"}

    @property
    def participants(self) -> List["MatchParticipantData"]:
        self.metaroot: Match
        return [p for p in self.metaroot.info.participants if p.team_id == self.id]


class MatchPerkSelectionData(PyotStatic):
    perk: int
    var1: int
    var2: int
    var3: int


class MatchPerkStyleData(PyotStatic):
    description: str
    selections: List[MatchPerkSelectionData]
    style: int


class MatchStatPerkData(PyotStatic):
    offense: int
    flex: int
    defense: int


class MatchPerkData(PyotStatic):
    stat_perks: MatchStatPerkData
    styles: List[MatchPerkStyleData]


class TimelineChampionStatData(PyotStatic):
    ability_haste: int
    ability_power: int
    armor: int
    armor_pen: int
    armor_pen_percent: int
    attack_damage: int
    attack_speed: int
    bonus_armor_pen_percent: int
    bonus_magic_pen_percent: int
    cc_reduction: int
    cooldown_reduction: int
    health: int
    health_max: int
    health_regen: int
    lifesteal: int
    magic_pen: int
    magic_pen_percent: int
    magic_resist: int
    movement_speed: int
    omnivamp: int
    physical_vamp: int
    power: int
    power_max: int
    power_regen: int
    spell_vamp: int


class TimelinePositionData(PyotStatic):
    x: int
    y: int


class TimelineDamageStatData(PyotStatic):
    magic_damage_done: int
    magic_damage_done_to_champions: int
    magic_damage_taken: int
    physical_damage_done: int
    physical_damage_done_to_champions: int
    physical_damage_taken: int
    total_damage_done: int
    total_damage_done_to_champions: int
    total_damage_taken: int
    true_damage_done: int
    true_damage_done_to_champions: int
    true_damage_taken: int


class TimelineParticipantFrameData(PyotStatic):
    champion_stats: TimelineChampionStatData
    current_gold: int
    damage_stats: TimelineDamageStatData
    gold_per_second: int
    jungle_minions_killed: int
    level: int
    minions_killed: int
    participant_id: int
    position: TimelinePositionData
    time_enemy_spent_controlled_millis: int
    total_gold: int
    xp: int

    class Meta(PyotStatic.Meta):
        renamed = {"time_enemy_spent_controlled": "time_enemy_spent_controlled_millis"}

    @property
    def time_enemy_spent_controlled(self) -> timedelta:
        return timedelta(milliseconds=self.time_enemy_spent_controlled_millis)


class TimelineVictimDamageData(PyotStatic):
    basic: bool
    magic_damage: int
    name: str
    participant_id: int
    physical_damage: int
    spell_name: str
    spell_slot: int
    true_damage: int
    type: str


class TimelineEventData(PyotStatic):
    actual_start_time_millis: int
    ascended_type: str
    assisting_participant_ids: List[int]
    after_id: int
    before_id: int
    bounty: int
    building_type: str
    creator_id: int
    event_type: str
    game_id: int
    gold_gain: int
    item_id: int
    kill_streak_length: int
    kill_type: str
    killer_id: int
    killer_team_id: int
    lane_type: str
    level: int
    level_up_type: str
    monster_type: str
    monster_sub_type: str
    multi_kill_length: int
    name: str
    participant_id: int
    point_captured: str
    position: TimelinePositionData
    real_timestamp: int
    skill_slot: int
    shutdown_bounty: int
    team_id: int
    timestamp: int
    transform_type: str
    type: str
    tower_type: str
    victim_id: int
    victim_damage_dealt: List[TimelineVictimDamageData]
    victim_damage_received: List[TimelineVictimDamageData]
    ward_type: str
    winning_team: int

    class Meta(PyotStatic.Meta):
        raws = {"assisting_participant_ids"}
        renamed = {"actual_start_time": "actual_start_time_millis"}

    @property
    def actual_start_time(self) -> timedelta:
        return timedelta(milliseconds=self.actual_start_time_millis)

    @property
    def time(self) -> timedelta:
        return timedelta(milliseconds=self.timestamp)

    @property
    def real_time(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp // 1000)

    @property
    def after_item(self) -> "Item":
        from .item import Item
        return Item(id=self.after_id)

    @property
    def item(self) -> "Item":
        from .item import Item
        return Item(id=self.item_id)

    @property
    def before_item(self) -> "Item":
        from .item import Item
        return Item(id=self.before_id)

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


class MatchParticipantData(PyotStatic):
    id: int
    assists: int
    baron_kills: int
    bounty_level: int
    champ_experience: int
    champ_level: int
    champion_id: int
    champion_name: str
    champion_transform: int
    consumables_purchased: int
    damage_dealt_to_buildings: int
    damage_dealt_to_objectives: int
    damage_dealt_to_turrets: int
    damage_self_mitigated: int
    deaths: int
    detector_wards_placed: int
    double_kills: int
    dragon_kills: int
    first_blood_assist: bool
    first_blood_kill: bool
    first_tower_assist: bool
    first_tower_kill: bool
    game_ended_in_early_surrender: bool
    game_ended_in_surrender: bool
    gold_earned: int
    gold_spent: int
    individual_position: str
    inhibitor_kills: int
    inhibitor_takedowns: int
    inhibitors_lost: int
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    items_purchased: int
    killing_sprees: int
    kills: int
    lane: str
    largest_critical_strike: int
    largest_killing_spree: int
    largest_multi_kill: int
    longest_time_spent_living_secs: int
    magic_damage_dealt: int
    magic_damage_dealt_to_champions: int
    magic_damage_taken: int
    neutral_minions_killed: int
    nexus_kills: int
    nexus_takedowns: int
    nexus_lost: int
    objectives_stolen: int
    objectives_stolen_assists: int
    penta_kills: int
    perks: MatchPerkData
    physical_damage_dealt: int
    physical_damage_dealt_to_champions: int
    physical_damage_taken: int
    profile_icon_id: int
    puuid: str
    quadra_kills: int
    riot_id_name: str
    riot_id_tagline: str
    role: str
    sight_wards_bought_in_game: int
    spell1_casts: int
    spell2_casts: int
    spell3_casts: int
    spell4_casts: int
    summoner1_casts: int
    summoner1_id: int
    summoner2_casts: int
    summoner2_id: int
    summoner_id: str
    summoner_level: int
    summoner_name: str
    team_early_surrendered: bool
    team_id: int
    team_position: str
    time_ccing_others_secs: int
    time_played_secs: int
    total_damage_dealt: int
    total_damage_dealt_to_champions: int
    total_damage_shielded_on_teammates: int
    total_damage_taken: int
    total_heal: int
    total_heals_on_teammates: int
    total_minions_killed: int
    total_time_cc_dealt_secs: int
    total_time_spent_dead_secs: int
    total_units_healed: int
    triple_kills: int
    true_damage_dealt: int
    true_damage_dealt_to_champions: int
    true_damage_taken: int
    turret_kills: int
    turret_takedowns: int
    turrets_lost: int
    unreal_kills: int
    vision_score: int
    vision_wards_bought_in_game: int
    wards_killed: int
    wards_placed: int
    challenges: Dict[str, float]
    frames: List[TimelineParticipantFrameData]
    events: List[TimelineEventData]
    win: bool

    class Meta(PyotStatic.Meta):
        raws = {'challenges'}
        renamed = {
            "participant_id": "id", "profile_icon": "profile_icon_id", "time_c_cing_others": "time_ccing_others_secs",
            "total_time_cc_dealt": "total_time_cc_dealt_secs", "total_time_spent_dead": "total_time_spent_dead_secs",
            "time_played": "time_played_secs", "longest_time_spent_living": "longest_time_spent_living_secs",
        }

    @property
    def total_time_cc_dealt(self) -> timedelta:
        return timedelta(seconds=self.total_time_cc_dealt_secs)

    @property
    def total_time_spent_dead(self) -> timedelta:
        return timedelta(seconds=self.total_time_spent_dead_secs)

    @property
    def time_ccing_others(self) -> timedelta:
        return timedelta(seconds=self.time_ccing_others_secs)

    @property
    def time_played(self) -> timedelta:
        return timedelta(seconds=self.time_played_secs)

    @property
    def longest_time_spent_living(self) -> timedelta:
        return timedelta(seconds=self.longest_time_spent_living_secs)

    @lazy_property
    def rune_ids(self) -> List[int]:
        ids = []
        for style in self.perks.styles:
            for selection in style.selections:
                ids.append(selection.perk)
        return ids

    @lazy_property
    def item_ids(self) -> List[int]:
        return [self.item0, self.item1, self.item2, self.item3, self.item4, self.item5, self.item6]

    @property
    def items(self) -> List["Item"]:
        from .item import Item
        return [Item(id=id_) for id_ in self.item_ids]

    @property
    def meraki_items(self) -> List["MerakiItem"]:
        from .merakiitem import MerakiItem
        return [MerakiItem(id=id_) for id_ in self.item_ids]

    @lazy_property
    def stat_rune_ids(self) -> List[int]:
        o = self.perks.stat_perks
        return [o.offense, o.flex, o.defense]

    @lazy_property
    def rune_primary_style(self) -> int:
        return next(style.style for style in self.perks.styles if style.description == "primaryStyle")

    @lazy_property
    def rune_sub_style(self) -> int:
        return next(style.style for style in self.perks.styles if style.description == "subStyle")

    @property
    def runes(self) -> List["Rune"]:
        from .rune import Rune
        return [Rune(id=id_) for id_ in self.rune_ids]

    @lazy_property
    def spell_ids(self) -> List[int]:
        return [self.summoner1_id, self.summoner2_id]

    @property
    def spells(self) -> List["Spell"]:
        from .spell import Spell
        return [Spell(id=id_) for id_ in self.spell_ids]

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(puuid=self.puuid, platform=self.metaroot.platform)


class MatchMetaData(PyotStatic):
    match_id: str
    data_version: str
    participant_puuids: List[str]

    class Meta(PyotStatic.Meta):
        raws = {"participant_puuids"}
        renamed = {"participants": "participant_puuids"}

    @property
    def participants(self) -> "Summoner":
        from .summoner import Summoner
        return [Summoner(puuid=puuid, platform=self.metaroot.platform) for puuid in self.participant_puuids]


class MatchInfoData(PyotStatic):
    game_id: int
    creation_millis: int
    duration_units: int
    start_millis: int
    end_millis: int
    mode: str
    name: str
    type: str
    version: str
    platform: str
    map_id: int
    queue_id: int
    tournament_code: str
    participants: List[MatchParticipantData]
    teams: List[MatchTeamData]

    class Meta(PyotStatic.Meta):
        renamed = {
            "game_creation": "creation_millis", "game_duration": "duration_units", "game_mode": "mode", "game_name": "name",
            "game_start_timestamp": "start_millis", "game_type": "type", "game_version": "version", "platform_id": "platform",
            "game_end_timestamp": "end_millis",
        }

    @property
    def creation(self) -> datetime:
        return datetime.fromtimestamp(self.creation_millis // 1000)

    @property
    def duration(self) -> timedelta:
        return timedelta(seconds=self.duration_secs)

    @property
    def start(self) -> datetime:
        return datetime.fromtimestamp(self.start_millis // 1000)

    @property
    def end(self) -> datetime:
        return datetime.fromtimestamp(self.end_millis // 1000)

    @property
    def duration_millis(self) -> int:
        if self.duration_units < 25200:
            return self.duration_units * 1000
        return self.duration_units

    @property
    def duration_secs(self) -> int:
        if self.duration_units > 25200:
            return self.duration_units / 1000
        return self.duration_units

    @property
    def start(self) -> datetime:
        return datetime.fromtimestamp(self.start_millis // 1000)


class TimelineFrameData(PyotStatic):
    events: List[TimelineEventData]
    participant_frames: List[TimelineParticipantFrameData]
    timestamp: int

    @property
    def time(self) -> timedelta:
        return timedelta(milliseconds=self.timestamp)


class TimelineParticipantData(PyotStatic):
    id: int
    puuid: str

    class Meta(PyotStatic.Meta):
        renamed = {"participant_id": "id"}

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(puuid=self.puuid, platform=self.metaroot.platform)


class TimelineInfoData(PyotStatic):
    frame_interval_millis: int
    frames: List[TimelineFrameData]
    game_id: int
    participants: List[TimelineParticipantData]

    class Meta(PyotStatic.Meta):
        renamed = {"frame_interval": "frame_interval_millis"}

    @property
    def frame_interval(self) -> timedelta:
        return timedelta(milliseconds=self.frame_interval_millis)


# PYOT CORE OBJECTS

class Match(PyotCore):
    metadata: MatchMetaData
    info: MatchInfoData
    id: str

    class Meta(PyotCore.Meta):
        rules = {"match_v5_match": ["id"]}

    def __init__(self, id: str, region: str = models.lol.DEFAULT_REGION):
        self.initialize(locals())

    @property
    def platform(self) -> str:
        try:
            return self.info.platform
        except AttributeError:
            return super().platform

    def feed_timeline(self, timeline: "Timeline", include_assisted=False, include_victim=False):
        '''Parse the given `Timeline` object's frames and events into this match's participants.
        - `include_assisted`: Include frames and events where the participants are scoring an assist.
        - `include_victim`: Include frames and events where the participants are victims.
        '''
        participants: Dict[int, MatchParticipantData] = {}
        for participant in self.info["participants"]:
            participants[participant["participantId"]] = participant
            participant["frames"] = []
            participant["events"] = []
        # print(participants)
        idkeys = ["participantId", "creatorId", "killerId"]
        for frame in timeline.info.frames:
            for participant_frame in frame["participantFrames"]:
                participants[participant_frame["participantId"]]["frames"].append(participant_frame)
            for event in frame["events"]:
                pid = None
                for idkey in idkeys:
                    pid = event.get(idkey, None)
                    if pid is not None:
                        break
                if not pid:
                    continue
                participants[pid]["events"].append(event)
                if include_assisted and "assistingParticipantIds" in event:
                    for apid in event["assistingParticipantIds"]:
                        participants[apid]["events"].append(event)
                if include_victim and "victimId" in event:
                    participants[event["victimId"]]["events"].append(event)


class Timeline(PyotCore):
    metadata: MatchMetaData
    info: TimelineInfoData
    id: str

    class Meta(PyotCore.Meta):
        rules = {"match_v5_timeline": ["id"]}

    def __init__(self, id: str, region: str = models.lol.DEFAULT_REGION):
        self.initialize(locals())

    def transform(self, data):
        data = data.copy()
        data["info"] = data["info"].copy()
        data["info"]["frames"] = data["info"]["frames"].copy()
        for i, f in enumerate(data["info"]["frames"]):
            data["info"]["frames"][i] = f.copy()
            data["info"]["frames"][i]["participantFrames"] = list(sorted(f["participantFrames"].values(), key=lambda p: p["participantId"]))
        return data

    @property
    def platform(self) -> "str":
        try:
            return self.metadata.match_id.split("_")[0]
        except AttributeError:
            return super().platform


class MatchHistory(PyotCore):
    ids: List[str]
    puuid: str

    class Meta(PyotCore.Meta):
        rules = {"match_v5_matches": ["puuid"]}
        raws = {"ids"}

    def __init__(self, puuid: str, region: str = models.lol.DEFAULT_REGION):
        self.initialize(locals())

    def __getitem__(self, item) -> Match:
        if not isinstance(item, int):
            return super().__getitem__(item)
        return Match(id=self.ids[item], region=self.region)

    def __iter__(self) -> Iterator[Match]:
        return iter(self.matches)

    def __len__(self) -> int:
        return len(self.ids)

    @property
    def matches(self) -> List[Match]:
        return [Match(id=id_, region=self.region) for id_ in self.ids]

    @property
    def timelines(self) -> List[Timeline]:
        return [Timeline(id=id_, region=self.region) for id_ in self.ids]

    @property
    def match_timelines(self) -> List[Tuple[Match, Timeline]]:
        return [(Match(id=id_, region=self.region), Timeline(id=id_, region=self.region)) for id_ in self.ids]

    def query(self, start: int = 0, count: int = 20, queue: int = None, type: str = None, start_time: Union[int, datetime] = None, end_time: Union[int, datetime] = None):
        '''Query parameters setter.'''
        if isinstance(start_time, datetime):
            start_time = int(start_time.timestamp())
        if isinstance(end_time, datetime):
            end_time = int(end_time.timestamp())
        self._meta.query = parse_camelcase(locals())
        return self

    def transform(self, data) -> Dict:
        return {"ids": data}
