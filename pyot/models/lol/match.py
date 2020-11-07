from .__core__ import PyotCore, PyotStatic
from datetime import datetime, timedelta
from typing import List, get_type_hints, Iterator
import asyncio


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
    rune_style: int
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
        renamed = {"time_c_cing_others": "time_ccing_others"}

    @property
    def items(self) -> List["Item"]:
        from .item import Item
        return [Item(id=i, locale=self.to_locale(self.platform)) for i in self.item_ids]

    @property
    def meraki_items(self) -> List["MerakiItem"]:
        from .merakiitem import MerakiItem
        return [MerakiItem(id=i) for i in self.item_ids]

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
    timestamp: timedelta
    assisting_participant_ids: List[int]
    building_type: str
    victim_id: int

    class Meta(PyotStatic.Meta):
        raws = ["assisting_participant_ids"]

    def __getattribute__(self, name):
        if name == "timestamp":
            return timedelta(super().__getattribute__(name))
        return super().__getattribute__(name)

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
    creeps_per_min_deltas: List[float]
    xp_per_min_deltas: List[float]
    gold_per_min_deltas: List[float]
    cs_diff_per_min_deltas: List[float]
    xp_diff_per_min_deltas: List[float]
    damage_taken_per_min_deltas: List[float]
    damage_taken_diff_per_min_deltas: List[float]
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
        return Summoner(account_id=self.account_id, platform=self.platform)

    @property
    def current_account(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(account_id=self.current_account_id, platform=self.current_platform)

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)

    @property
    def profile_icon(self) -> "ProfileIcon":
        from .profileicon import ProfileIcon
        return ProfileIcon(id=self.profile_icon_id, locale=self.to_locale(self.platform))


class MatchTeamData(PyotStatic):
    team_id: int
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


class MatchHistoryData(PyotStatic):
    platform: str
    id: int
    champion_id: int
    queue_id: int
    season_id: int
    creation: datetime
    role: str
    lane: str

    class Meta(PyotStatic.Meta):
        renamed = {"platform_id": "platform", "game_id": "id", "champion": "champion_id", "queue": "queue_id",
            "season": "season_id", "timestamp": "creation"}

    def __getattribute__(self, name):
        if name == "creation":
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        return super().__getattribute__(name)

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
    def match_timeline(self) -> "MatchTimeline":
        return MatchTimeline(id=self.id, platform=self.platform)

    @property
    def timeline(self) -> "Timeline":
        return Timeline(id=self.id, platform=self.platform)


class MatchFrameMinuteData(PyotStatic):
    frame: List[MatchFrameData]

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.frame[item]

    def __iter__(self) -> Iterator[MatchFrameData]:
        return iter(self.frame)

    def __len__(self):
        return len(self.frame)


class MatchEventMinuteData(PyotStatic):
    frame: List[MatchEventData]

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.frame[item]

    def __iter__(self) -> Iterator[MatchEventData]:
        return iter(self.frame)

    def __len__(self):
        return len(self.frame)


# PYOT CORE OBJECTS

class Match(PyotCore):
    id: int
    type: str
    mode: str
    version: str
    map_id: int
    season_id: int
    queue_id: int
    creation: datetime
    duration: timedelta #not milliseconds
    platform: str
    teams: List[MatchTeamData]
    blue_team: MatchTeamData
    red_team: MatchTeamData

    class Meta(PyotCore.Meta):
        rules = {"match_v4_match": ["id"]}
        renamed = {"game_id": "id", "platform_id": "platform", "game_creation": "creation", "game_duration": "duration",
            "game_version": "version", "game_mode": "mode", "game_type": "type", "queue": "queue_id"}

    def __getattribute__(self, name):
        if name == "creation":
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        elif name == "duration":
            return timedelta(seconds=super().__getattribute__(name))
        return super().__getattribute__(name)

    def __init__(self, id: int = None, platform: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        if data["teams"][0]["teamId"] == 100:
            blue_team = data["teams"][0]
            red_team = data["teams"][1]
        elif data["teams"][0]["teamId"] == 200:
            red_team = data["teams"][0]
            blue_team = data["teams"][1]
        else:
            blue_team = data["teams"][0]
            red_team = data["teams"][1]

        blue_team["participants"] = []
        red_team["participants"] = []

        if blue_team["win"] == "Win":
            blue_team["win"] = True
        else:
            blue_team["win"] = False
        
        if red_team["win"] == "Win":
            red_team["win"] = True
        else:
            red_team["win"] = False

        for p in data["participants"]:
            p["spellIds"] = [p.pop("spell1Id"), p.pop("spell2Id")]
            stats = p["stats"]
            stats["spellIds"] = p["spellIds"]
            
            stats["dominionScores"] = []
            for i in range(10):
                score = stats.pop("playerScore"+str(i))
                stats["dominionScores"].append(score)
            
            stats["itemIds"] = []
            for i in range(7):
                item = stats.pop("item"+str(i))
                stats["itemIds"].append(item)

            stats["runeIds"] = []
            stats["runeVars"] = []
            for i in range(6):
                rune = stats.pop("perk"+str(i))
                stats["runeIds"].append(rune)
                statset = []
                for j in range(1, 4):
                    st = stats.pop("perk"+str(i)+"Var"+str(j))
                    statset.append(st)
                stats["runeVars"].append(statset)
            
            stats["runeStyle"] = stats.pop("perkPrimaryStyle", None)
            stats["runeSubStyle"] = stats.pop("perkSubStyle", None)

            stats["statRuneIds"] = []
            for i in range(3):
                statrune = stats.pop("statPerk"+str(i))
                stats["statRuneIds"].append(statrune)

            timeline = p["timeline"]

            for key, val in timeline.items():
                if "Deltas" in key:
                    deltaset = []
                    for i in range(6):
                        try: deltaset.append(val[f"{i*10}-{i*10+10}"])
                        except KeyError: break
                    timeline[key] = deltaset
            
            if p["teamId"] == 100:
                blue_team["participants"].append(p)
            elif p["teamId"] == 200:
                red_team["participants"].append(p)

        for pi in data["participantIdentities"]:
            if pi["player"]["platformId"].lower() == "na":
                pi["player"]["platformId"] = "NA1"
            if pi["player"]["currentPlatformId"].lower() == "na":
                pi["player"]["currentPlatformId"] = "NA1"
            pid = pi["participantId"]
            for p in blue_team["participants"]:
                if p["participantId"] == pid:
                    p.update(pi["player"])
            for p in red_team["participants"]:
                if p["participantId"] == pid:
                    p.update(pi["player"])
        
        data.pop("participants")
        data.pop("participantIdentities")
        data["blueTeam"] = blue_team
        data["redTeam"] = red_team
        return data


class MatchTimeline(Match, PyotCore):
    
    class Meta(Match.Meta):
        rules = {
            "match_v4_match": ["id"],
            "match_v4_timeline": ["id"],
        }

    async def get(self, sid: str = None, pipeline: str = None):
        '''Awaitable. Get this object from the pipeline.\n
        `sid` id identifying the session on the pipeline to reuse.\n
        `pipeline` key identifying the pipeline to execute against.\n
        '''
        # pylint: disable=no-member
        if pipeline:
            self.set_pipeline(pipeline)
        token1 = await self.create_token(search="match")
        token2 = await self.create_token(search="timeline")
        task1 = asyncio.create_task(self._meta.pipeline.get(token1, sid))
        task2 = asyncio.create_task(self._meta.pipeline.get(token2, sid))
        data1 = await task1
        data2 = await task2
        self._meta.data = self._transform(data1, data2)
        self._fill()
        return self

    def _transform(self, data1, data2):
        data = super()._transform(data1)
        teams = data["teams"]
        frames = {}
        events = {}
        for val in data2["frames"][0]["participantFrames"].values():
            frames[val["participantId"]] = []
            events[val["participantId"]] = []
        for frame in data2["frames"]:
            for key, val in frame["participantFrames"].items():
                p = val["participantId"]
                frames[p].append(val)
            for event in frame["events"]:
                p = 0
                if "participantId" in event:
                    p = int(event["participantId"])
                elif "creatorId" in event:
                    p = int(event["creatorId"])
                elif "killerId" in event:
                    p = int(event["killerId"])
                if p != 0:
                    events[p].append(event)
        for key in frames:
            for i in range(len(teams)):
                found = False
                for j in range(len(teams[i]["participants"])):
                    if teams[i]["participants"][j]["participantId"] == key:
                        teams[i]["participants"][j]["timeline"]["frames"] = frames[key]
                        teams[i]["participants"][j]["timeline"]["events"] = events[key]
                        found = True
                        break
                if found: break
        return data


class Timeline(PyotCore):
    frames: List[MatchFrameMinuteData]
    events: List[MatchEventMinuteData]
    interval: timedelta

    class Meta(PyotCore.Meta):
        rules = {"match_v4_timeline": ["id"]}

    def __getattribute__(self, name):
        if name == "interval":
            return timedelta(milliseconds=super().__getattribute__(name))
        return super().__getattribute__(name)

    def __init__(self, id: int = None, platform: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        new_data = {
            "frames": {},
            "events": {},
            "interval": data["frameInterval"]
        }
        for f in data["frames"]:
            new_data["frames"]["frame"] = list(f["participantFrames"].values())
            new_data["events"]["frame"] = f["events"]
        return new_data


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
        kargs = {key if key[-3:] != "ids" else key[:-3] : val for (key,val) in locals().items()}
        for i in [champion_ids, queue_ids, season_ids]:
            if not isinstance(i, list) and i is not None:
                raise RuntimeError("Query parameters 'champion_ids', 'queue_ids' and 'season_ids' must be a list of values")
        self._meta.query = self._parse_camel(kargs)
        return self

    @property
    def matches(self) -> List[Match]:
        return [Match(id=entry.id, platform=entry.platform) for entry in self.entries]

    @property
    def match_timelines(self) -> List[MatchTimeline]:
        return [MatchTimeline(id=entry.id, platform=entry.platform) for entry in self.entries]

    @property
    def timelines(self) -> List[Timeline]:
        return [Timeline(id=entry.id, platform=entry.platform) for entry in self.entries]

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(account_id=self.account_id, platform=self.platform)
