from .__core__ import PyotCore, PyotStatic
from datetime import datetime, timedelta
from typing import List, Iterator


# PYOT STATIC OBJECTS

class MatchInfoData(PyotStatic):
    id: str
    map_id: str
    duration: timedelta
    creation: datetime
    provisioning_flow_id: str
    is_completed: bool
    custom_game_name: str
    queue_id: str
    game_mode: str
    is_ranked: bool
    season_id: str

    class Meta(PyotStatic.Meta):
        renamed = {"game_length_millis": "duration", "game_start_millis": "creation", "match_id": "id"}

    def __getattribute__(self, name):
        if name == "creation":
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        elif name == "duration":
            return timedelta(milliseconds=super().__getattribute__(name))
        return super().__getattribute__(name)


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
    playtime: timedelta
    ability_casts: MatchPlayerAbilityCastData

    class Meta(PyotStatic.Meta):
        renamed = {"playtime_millis": "playtime"}

    def __getattribute__(self, name):
        if name == "playtime":
            return timedelta(milliseconds=super().__getattribute__(name))
        return super().__getattribute__(name)


class MatchPlayerData(PyotStatic):
    puuid: str
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
        return Account(puuid=self.puuid, region=self.region).set_pipeline("val")


class MatchTeamData(PyotStatic):
    id: str
    won: bool
    rounds_played: int
    rounds_won: int

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
    game_duration: timedelta
    round_duration: timedelta
    killer_puuid: str
    victim_puuid: str
    victim_location: MatchLocationData	
    assistant_puuids: List[str]
    player_locations: List[MatchPlayerLocationData]
    finishing_damage: MatchPlayerFinishingDamageData

    class Meta(PyotStatic.Meta):
        raws = ["assistant_puuids"]
        renamed = {"killer": "killer_puuid", "victim": "victim_puuid", "assistants": "assistant_puuids",
            "time_since_game_start_millis": "game_duration", "time_since_round_start_millis": "round_duration"}

    def __getattribute__(self, name):
        if name in ["game_duration", "round_duration"]:
            return timedelta(milliseconds=super().__getattribute__(name))
        return super().__getattribute__(name)

    @property
    def killer(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.killer_puuid, region=self.region).set_pipeline("val")

    @property
    def victim(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.victim_puuid, region=self.region).set_pipeline("val")

    @property
    def assistants(self) -> List["Account"]:
        from ..riot.account import Account
        return [Account(puuid=i, region=self.region).set_pipeline("val") for i in self.assistant_puuids]


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
    plant_round_time: timedelta
    plant_player_locations: List[MatchPlayerLocationData]
    plant_location: MatchLocationData
    plant_site: str
    defuse_round_time: timedelta
    defuse_player_locations: List[MatchPlayerLocationData]
    defuse_location: MatchLocationData
    player_stats: List[MatchPlayerRoundStatData]
    round_result_code: str

    class Meta(PyotStatic.Meta):
        renamed = {"bomb_planter": "bomb_planter_puuid", "bomb_defuser": "bomb_defuser_puuid"}

    def __getattribute__(self, name):
        if name in ["plant_round_time", "defuse_round_time"]:
            return timedelta(milliseconds=super().__getattribute__(name))
        return super().__getattribute__(name)

    @property
    def bomb_planter(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.bomb_planter_puuid, region=self.region).set_pipeline("val")

    @property
    def bomb_defuser(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.bomb_defuser_puuid, region=self.region).set_pipeline("val")


# PYOT CORE OBJECTS

class Match(PyotCore):
    id: str
    info: MatchInfoData
    players: List[MatchPlayerData]
    teams: List[MatchTeamData]
    round_results: List[MatchRoundResultData]
    # <~> MatchHistory
    creation: datetime
    team_id: str

    class Meta(PyotCore.Meta):
        renamed = {"match_info": "info", "game_start_time_millis": "creation", "match_id": "id"}
        rules = {"match_v1_match": ["id"]}

    def __getattribute__(self, name):
        if name == "creation":
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        return super().__getattribute__(name)

    def __init__(self, id: str = None, platform: str = None):
        self._lazy_set(locals())


class MatchHistory(PyotCore):
    puuid: str
    history: List[Match]

    class Meta(PyotCore.Meta):
        rules = {"match_v1_matchlist": ["puuid"]}

    def __init__(self, puuid: str = None, platform: str = None):
        self._lazy_set(locals())

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
        return Account(puuid=self.puuid, region=self.region).set_pipeline("val")


class RecentMatches(PyotCore):
    current_time: datetime
    match_ids: List[str]

    class Meta(PyotCore.Meta):
        raws = ["match_ids"]
        rules = {"match_v1_recent": ["queue"]}

    def __getattribute__(self, name):
        if name == "current_time":
            return datetime.fromtimestamp(super().__getattribute__(name))
        return super().__getattribute__(name)

    def __init__(self, queue: str = None, platform: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.matches[item]

    def __iter__(self) -> Iterator["Match"]:
        return iter(self.matches)

    def __len__(self):
        return len(self.matches)

    @property
    def matches(self) -> List["Match"]:
        return [Match(id=id_, platform=self.platform) for id_ in self.match_ids]
