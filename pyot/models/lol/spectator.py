from typing import List, Iterator, TYPE_CHECKING
from datetime import datetime, timedelta

from pyot.conf.model import models
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from .champion import Champion
    from .merakichampion import MerakiChampion
    from .rune import Rune
    from .spell import Spell
    from .summoner import Summoner
    from .profileicon import ProfileIcon


# PYOT STATIC OBJECTS

class CurrentGameBansData(PyotStatic):
    pick_turn: int
    champion_id: int
    team_id: int

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id)

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)


class CurrentGameParticipantCustomizationData(PyotStatic):
    category: str
    content: str


class CurrentGameParticipantData(PyotStatic):
    team_id: int
    champion_id: int
    profile_icon_id: int
    is_bot: bool
    summoner_name: str
    summoner_id: str
    spell_ids: List[int]
    rune_ids: List[int]
    rune_main_style: int
    rune_sub_style: int
    game_customization_objects: List[CurrentGameParticipantCustomizationData]
    position: str

    class Meta(PyotStatic.Meta):
        renamed = {"bot": "is_bot", "perk_ids": "rune_ids", "perk_style": "rune_main_style", "perk_sub_style": "rune_sub_style"}
        raws = {"spell_ids", "rune_ids"}

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, name=self.summoner_name, platform=self.platform)

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id)

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)

    @property
    def profile_icon(self) -> "ProfileIcon":
        from .profileicon import ProfileIcon
        return ProfileIcon(id=self.profile_icon_id)

    @property
    def runes(self) -> List["Rune"]:
        from .rune import Rune
        mutable = []
        for i in self.rune_ids:
            mutable.append(Rune(id=i))
        return mutable

    @property
    def spells(self) -> List["Spell"]:
        from .spell import Spell
        mutable = []
        for i in self.spell_ids:
            mutable.append(Spell(id=i))
        return mutable


class FeaturedGameParticipantData(PyotStatic):
    team_id: int
    champion_id: int
    profile_icon_id: int
    is_bot: bool
    summoner_name: str
    spell_ids: List[int]
    position: str

    class Meta(PyotStatic.Meta):
        renamed = {"bot": "is_bot"}
        raws = {"spell_ids"}

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(name=self.summoner_name, platform=self.platform)

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id)

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)

    @property
    def profile_icon(self) -> "ProfileIcon":
        from .profileicon import ProfileIcon
        return ProfileIcon(id=self.profile_icon_id)

    @property
    def spells(self) -> List["Spell"]:
        from .spell import Spell
        mutable = []
        for i in self.spell_ids:
            mutable.append(Spell(id=i))
        return mutable


class CurrentGameTeamData(PyotStatic):
    id: int
    bans: List[CurrentGameBansData]
    participants: List[CurrentGameParticipantData]


class FeaturedGameTeamData(PyotStatic):
    id: int
    bans: List[CurrentGameBansData]
    participants: List[FeaturedGameParticipantData]


class FeaturedGameData(PyotStatic):
    id: int
    type: str
    mode: str
    start_time_millis: int
    length_secs: int #not milliseconds
    map_id: int
    platform: str
    queue_id: int
    observers_key: str
    teams: List[FeaturedGameTeamData]

    class Meta(PyotStatic.Meta):
        renamed = {"game_id": "id", "game_type": "type", "game_start_time": "start_time_millis", "game_mode": "mode",
            "game_length": "length_secs", "platform_id": "platform", "game_queue_config_id": "queue_id"}

    @property
    def start_time(self) -> datetime:
        return datetime.fromtimestamp(self.start_time_millis//1000)

    @property
    def length(self) -> timedelta:
        return timedelta(seconds=self.length_secs)

    @property
    def banned_champions(self) -> List[CurrentGameBansData]:
        bans = []
        for team in self.teams:
            bans += team.bans
        return bans

    @property
    def participants(self) -> List[FeaturedGameParticipantData]:
        participants = []
        for team in self.teams:
            participants += team.participants
        return participants

    @property
    def blue_team(self) -> FeaturedGameTeamData:
        return self.teams[0]

    @property
    def red_team(self) -> FeaturedGameTeamData:
        return self.teams[1]


# PYOT CORE OBJECTS

class CurrentGame(FeaturedGameData, PyotCore):
    summoner_id: str
    teams: List[CurrentGameTeamData]

    class Meta(FeaturedGameData.Meta, PyotCore.Meta):
        rules = {"spectator_v4_current_game": ["summoner_id"]}

    def __init__(self, summoner_id: str = None, platform: str = models.lol.DEFAULT_PLATFORM):
        self.initialize(locals())

    def transform(self, data):
        data = data.copy()
        data["teams"] = [{"id": 100, "bans": [], "participants": []}, {"id": 200, "bans": [], "participants": []}]
        data["observersKey"] = data.pop("observers", None)["encryptionKey"]
        for ban in data.pop("bannedChampions", []):
            if ban["teamId"] == 100:
                data["teams"][0]["bans"].append(ban)
            else:
                data["teams"][1]["bans"].append(ban)
        for p in data.pop("participants", []).copy():
            p = p.copy()
            p["spellIds"] = [p.pop("spell1Id", None), p.pop("spell2Id", None)]
            p.update(p.pop("perks", {}))
            if p["teamId"] == 100:
                data["teams"][0]["participants"].append(p)
            else:
                data["teams"][1]["participants"].append(p)
        return data

    @property
    def banned_champions(self) -> List[CurrentGameBansData]:
        bans = []
        for team in self.teams:
            bans += team.bans
        return bans

    @property
    def participants(self) -> List[CurrentGameParticipantData]:
        participants = []
        for team in self.teams:
            participants += team.participants
        return participants

    @property
    def blue_team(self) -> CurrentGameTeamData:
        return self.teams[0]

    @property
    def red_team(self) -> CurrentGameTeamData:
        return self.teams[1]

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)


class FeaturedGames(PyotCore):
    games: List[FeaturedGameData]
    refresh_interval_secs: int

    class Meta(PyotCore.Meta):
        rules = {"spectator_v4_featured_games": []}
        renamed = {"client_refresh_interval": "refresh_interval_secs", "game_list": "games"}

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.games[item]

    def __iter__(self) -> Iterator[FeaturedGameData]:
        return iter(self.games)

    def __len__(self):
        return len(self.games)

    def __init__(self, platform: str = models.lol.DEFAULT_PLATFORM):
        self.initialize(locals())

    def transform(self, data):
        data = data.copy()
        data["gameList"] = data["gameList"].copy()
        for ind, game in enumerate(data["gameList"]):
            data["gameList"][ind] = CurrentGame.transform(self, game)
        return data

    @property
    def refresh_interval(self) -> timedelta:
        return timedelta(seconds=self.refresh_interval_secs)
