from datetime import datetime, timedelta
from typing import List, Iterator, TYPE_CHECKING

from pyot.conf.model import models
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from ..riot.account import Account


# PYOT STATIC OBJECTS

class MatchInfoData(PyotStatic):
    id: str
    map_id: str
    start_millis: int
    length_millis: int
    provisioning_flow_id: str
    is_completed: bool
    custom_game_name: str
    queue_id: str
    game_mode: str
    is_ranked: bool
    season_id: str

    class Meta(PyotStatic.Meta):
        renamed = {"game_length_millis": "length_millis", "game_start_millis": "start_millis", "match_id": "id"}

    @property
    def start(self) -> datetime:
        return datetime.fromtimestamp(self.start_millis//1000)

    @property
    def length(self) -> timedelta:
        return timedelta(seconds=self.length_millis)


class MatchPlayerAbilityCastData(PyotStatic):
    grenade_casts: int
    ability1_casts: int
    ability2_casts: int
    ultimate_casts: int


class MatchPlayerAbilityData(PyotStatic):
    grenade_effects: int
    ability1_effects: int
    ability2_effects: int
    ultimate_effects: int


class MatchPlayerStatData(PyotStatic):
    score: int
    rounds_played: int
    kills: int
    deaths: int
    assists: int
    playtime_millis: int
    ability_casts: MatchPlayerAbilityCastData

    @property
    def playtime(self) -> timedelta:
        return timedelta(milliseconds=self.playtime_millis)


class MatchPlayerData(PyotStatic):
    puuid: str
    game_name: str
    tag_line: str
    team_id: str
    party_id: str
    character_id: str
    stats: MatchPlayerStatData
    competitive_tier: int
    player_card: str
    player_title: str

    @property
    def account(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.puuid).pipeline(self.metapipeline.name)


class MatchTeamData(PyotStatic):
    id: str
    won: bool
    rounds_played: int
    rounds_won: int
    num_points: int

    class Meta(PyotStatic.Meta):
        renamed = {"team_id": "id"}


class MatchLocationData(PyotStatic):
    x: int
    y: int


class MatchPlayerLocationData(PyotStatic):
    puuid: str
    view_radians: float
    location: MatchLocationData


class MatchPlayerFinishingDamageData(PyotStatic):
    damage_type: str
    damage_item: str
    is_secondary_fire_mode: bool


class MatchPlayerKillData(PyotStatic):
    game_time_millis: int
    round_time_millis: int
    killer_puuid: str
    victim_puuid: str
    victim_location: MatchLocationData
    assistant_puuids: List[str]
    player_locations: List[MatchPlayerLocationData]
    finishing_damage: MatchPlayerFinishingDamageData

    class Meta(PyotStatic.Meta):
        raws = {"assistant_puuids"}
        renamed = {"killer": "killer_puuid", "victim": "victim_puuid", "assistants": "assistant_puuids",
            "time_since_game_start_millis": "game_time_millis", "time_since_round_start_millis": "round_time_millis"}

    @property
    def game_time(self) -> timedelta:
        return timedelta(milliseconds=self.game_time_millis)

    @property
    def round_time(self) -> timedelta:
        return timedelta(milliseconds=self.round_time_millis)

    @property
    def killer(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.killer_puuid).pipeline(self.metapipeline.name)

    @property
    def victim(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.victim_puuid).pipeline(self.metapipeline.name)

    @property
    def assistants(self) -> List["Account"]:
        from ..riot.account import Account
        return [Account(puuid=i).pipeline(self.metapipeline.name) for i in self.assistant_puuids]


class MatchPlayerDamageData(PyotStatic):
    receiver: str
    damage: int
    legshots: int
    bodyshots: int
    headshots: int


class MatchPlayerEconomyData(PyotStatic):
    loadout_value: int
    weapon: str
    armor: str
    remaining: int
    spent: int


class MatchPlayerRoundStatData(PyotStatic):
    puuid: str
    kills: List[MatchPlayerKillData]
    damage: List[MatchPlayerDamageData]
    score: int
    economy: MatchPlayerEconomyData
    ability: MatchPlayerAbilityData


class MatchRoundResultData(PyotStatic):
    round_num: int
    round_result: str
    round_ceremony: str
    winning_team: str
    bomb_planter_puuid: str
    bomb_defuser_puuid: str
    plant_round_millis: int
    plant_player_locations: List[MatchPlayerLocationData]
    plant_location: MatchLocationData
    plant_site: str
    defuse_round_millis: int
    defuse_player_locations: List[MatchPlayerLocationData]
    defuse_location: MatchLocationData
    player_stats: List[MatchPlayerRoundStatData]
    round_result_code: str

    class Meta(PyotStatic.Meta):
        renamed = {"bomb_planter": "bomb_planter_puuid", "bomb_defuser": "bomb_defuser_puuid",
            "plant_round_time": "plant_round_millis", "defuse_round_time": "defuse_round_millis"}

    @property
    def plant_round_time(self) -> timedelta:
        return timedelta(milliseconds=self.plant_round_millis)

    @property
    def defuse_round_time(self) -> timedelta:
        return timedelta(milliseconds=self.defuse_round_millis)

    @property
    def bomb_planter(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.bomb_planter_puuid).pipeline(self.metapipeline.name)

    @property
    def bomb_defuser(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.bomb_defuser_puuid).pipeline(self.metapipeline.name)


class MatchCoachData(PyotStatic):
    puuid: str
    team_id: str


# PYOT CORE OBJECTS

class Match(PyotCore):
    id: str
    info: MatchInfoData
    players: List[MatchPlayerData]
    teams: List[MatchTeamData]
    coaches: List[MatchCoachData]
    round_results: List[MatchRoundResultData]
    # <~> MatchHistory
    start_time_millis: int
    team_id: str
    queue_id: str

    class Meta(PyotCore.Meta):
        renamed = {"match_info": "info", "game_start_time_millis": "start_time_millis", "match_id": "id"}
        rules = {"match_v1_match": ["id"]}

    def __init__(self, id: str = None, platform: str = models.val.DEFAULT_PLATFORM):
        self.initialize(locals())

    @property
    def start_time(self) -> datetime:
        return datetime.fromtimestamp(self.start_time_millis//1000)


class MatchHistory(PyotCore):
    puuid: str
    history: List[Match]

    class Meta(PyotCore.Meta):
        rules = {"match_v1_matchlist": ["puuid"]}

    def __init__(self, puuid: str = None, platform: str = models.val.DEFAULT_PLATFORM):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.history[item]

    def __iter__(self) -> Iterator[Match]:
        return iter(self.history)

    def __len__(self):
        return len(self.history)

    @property
    def account(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.puuid).pipeline(self.metapipeline.name)


class RecentMatches(PyotCore):
    current_timestamp: int
    match_ids: List[str]

    class Meta(PyotCore.Meta):
        raws = {"match_ids"}
        rules = {"match_v1_recent": ["queue"]}
        renamed = {"current_time": "current_timestamp"}

    def __init__(self, queue: str = None, platform: str = models.val.DEFAULT_PLATFORM):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.matches[item]

    def __iter__(self) -> Iterator[Match]:
        return iter(self.matches)

    def __len__(self):
        return len(self.matches)

    @property
    def current_time(self) -> datetime:
        return datetime.fromtimestamp(self.current_timestamp)

    @property
    def matches(self)  -> List[Match]:
        return [Match(id=id_, platform=self.platform) for id_ in self.match_ids]
