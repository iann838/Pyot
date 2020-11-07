from .__core__ import PyotCore, PyotStatic
from typing import List, Iterator
from datetime import datetime, timedelta
import copy


# PYOT STATIC OBJECTS

class CurrentGameBansData(PyotStatic):
    pick_turn: int
    champion_id: int

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id, locale=self.to_locale(self.platform))

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)


class CurrentGameParticipantData(PyotStatic):
    team_id: int
    champion_id: int
    profile_icon_id: int
    is_bot: bool
    summoner_name: str
    summoner_id: str
    spell_ids: List[int]
    rune_ids: List[int]
    rune_style: int
    rune_sub_style: int

    class Meta(PyotStatic.Meta):
        renamed = {"bot": "is_bot", "perk_ids": "rune_ids", "perk_style": "rune_style", "perk_sub_style": "rune_sub_style"}
        raws = ["spell_ids", "rune_ids"]

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, name=self.summoner_name, platform=self.platform)

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id, locale=self.to_locale(self.platform))

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)

    @property
    def profile_icon(self) -> "ProfileIcon":
        from .profileicon import ProfileIcon
        return ProfileIcon(id=self.profile_icon_id, locale=self.to_locale(self.platform))

    @property
    def runes(self) -> List["Rune"]:
        from .rune import Rune
        mutable = []
        for i in self.rune_ids:
            mutable.append(Rune(id=i, locale=self.to_locale(self.platform)))
        return mutable

    @property
    def spells(self) -> List["Spell"]:
        from .spell import Spell
        mutable = []
        for i in self.spell_ids:
            mutable.append(Spell(id=i, locale=self.to_locale(self.platform)))
        return mutable


class FeaturedGameParticipantData(PyotStatic):
    team_id: int
    champion_id: int
    profile_icon_id: int
    is_bot: bool
    summoner_name: str
    spell_ids: List[int]

    class Meta(PyotStatic.Meta):
        renamed = {"bot": "is_bot"}
        raws = ["spell_ids"]

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(name=self.summoner_name, platform=self.platform)

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id, locale=self.to_locale(self.platform))

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)
        
    @property
    def profile_icon(self) -> "ProfileIcon":
        from .profileicon import ProfileIcon
        return ProfileIcon(id=self.profile_icon_id, locale=self.to_locale(self.platform))

    @property
    def spells(self) -> List["Spell"]:
        from .spell import Spell
        mutable = []
        for i in self.spell_ids:
            mutable.append(Spell(id=i, locale=self.to_locale(self.platform)))
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
    creation: datetime
    duration: timedelta #not milliseconds
    map_id: int
    platform: str
    queue: int
    observers_key: str
    teams: List[FeaturedGameTeamData]
    blue_team: FeaturedGameTeamData
    red_team: FeaturedGameTeamData

    class Meta(PyotStatic.Meta):
        renamed = {"game_id": "id", "game_type": "type", "game_start_time": "creation", "game_mode": "mode",
            "game_length": "duration", "platform_id": "platform", "game_queue_config_id": "queue"}
    
    def __getattribute__(self, name):
        if name == "creation":
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        elif name == "duration":
            return timedelta(seconds=super().__getattribute__(name))
        return super().__getattribute__(name)


# PYOT CORE OBJECTS

class CurrentGame(FeaturedGameData, PyotCore):
    summoner_id: str
    teams: List[CurrentGameTeamData]

    class Meta(FeaturedGameData.Meta, PyotCore.Meta):
        rules = {"spectator_v4_current_game": ["summoner_id"]}

    def __init__(self, summoner_id: str = None, platform: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        data["teams"] = [{"id": 100, "bans": [], "participants": []}, {"id": 200, "bans": [], "participants": []}]
        data["observersKey"] = None
        for attr, val in data.items():
            if attr == "bannedChampions":
                for ban in val:
                    if ban["teamId"] == 100:
                        ban.pop("teamId")
                        data["teams"][0]["bans"].append(ban)
                    elif ban["teamId"] == 200:
                        ban.pop("teamId")
                        data["teams"][1]["bans"].append(ban)
                    else:
                        raise RuntimeError
            elif attr == "participants":
                for p in val:
                    p.pop("gameCustomizationObjects")
                    p["spellIds"] = [p.pop("spell1Id"), p.pop("spell2Id")]
                    p.update(p.pop("perks"))
                    if p["teamId"] == 100:
                        data["teams"][0]["participants"].append(p)
                    elif p["teamId"] == 200:
                        data["teams"][1]["participants"].append(p)
                    else:
                        raise RuntimeError
            elif attr == "observers":
                data["observersKey"] = val["encryptionKey"]
            elif attr == "teams":
                pass
            else:
                data[attr] = val
        data.pop("bannedChampions", None)
        data.pop("participants", None)
        data.pop("observers", None)
        data["blueTeam"] = data["teams"][0]
        data["redTeam"] = data["teams"][1]
        return data

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)


class FeaturedGames(PyotCore):
    games: List[FeaturedGameData]
    refresh_interval: timedelta

    class Meta(PyotCore.Meta):
        rules = {"spectator_v4_featured_games": []}
        renamed = {"client_refresh_interval": "refresh_interval", "game_list": "games"}

    def __getattribute__(self, name):
        if name == "refresh_interval":
            return timedelta(seconds=super().__getattribute__(name))
        return super().__getattribute__(name)

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.games[item]

    def __iter__(self) -> Iterator[FeaturedGameData]:
        return iter(self.games)

    def __len__(self):
        return len(self.games)

    def __init__(self, platform: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        for i in range(len(data["gameList"])):
            data["gameList"][i]["teams"] = [{"id": 100, "bans": [], "participants": []}, {"id": 200, "bans": [], "participants": []}]
            data["gameList"][i]["observersKey"] = None
            for attr, val in data["gameList"][i].items():
                if attr == "bannedChampions":
                    for ban in val:
                        if ban["teamId"] == 100:
                            ban.pop("teamId")
                            data["gameList"][i]["teams"][0]["bans"].append(ban)
                        elif ban["teamId"] == 200:
                            ban.pop("teamId")
                            data["gameList"][i]["teams"][1]["bans"].append(ban)
                        else:
                            raise RuntimeError
                elif attr == "participants":
                    for p in val:
                        p["spellIds"] = [p.pop("spell1Id"), p.pop("spell2Id")]
                        if p["teamId"] == 100:
                            data["gameList"][i]["teams"][0]["participants"].append(p)
                        elif p["teamId"] == 200:
                            data["gameList"][i]["teams"][1]["participants"].append(p)
                        else:
                            raise RuntimeError
                elif attr == "observers":
                    data["gameList"][i]["observersKey"] = val["encryptionKey"]
                elif attr == "teams":
                    pass
                else:
                    data["gameList"][i][attr] = val
            data["gameList"][i].pop("bannedChampions", None)
            data["gameList"][i].pop("participants", None)
            data["gameList"][i].pop("observers", None)
            data["gameList"][i]["blueTeam"] = data["gameList"][i]["teams"][0]
            data["gameList"][i]["redTeam"] = data["gameList"][i]["teams"][1]
        return data
