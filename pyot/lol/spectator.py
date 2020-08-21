from .__core__ import PyotCore, PyotStatic
from typing import List
from datetime import datetime, timedelta
import copy


# PYOT STATIC OBJECTS

class CurrentGameBansData(PyotStatic):
    pick_turn: int
    champion_id: int


class CurrentGameParticipantData(PyotStatic):
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


class FeaturedGameParticipantData(PyotStatic):
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
        rules = {"spectator-v4-current-game": ["summoner_id"]}

    def __init__(self, summoner_id: str = None, platform: str = None):
        self._lazy_set(locals())

    async def _transform(self, data_):
        data = copy.deepcopy(data_)
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
                        p.pop("teamId")
                        data["teams"][0]["participants"].append(p)
                    elif p["teamId"] == 200:
                        p.pop("teamId")
                        data["teams"][1]["participants"].append(p)
                    else:
                        raise RuntimeError
            elif attr == "observers":
                data["observersKey"] = val["encryptionKey"]
            elif attr == "teams":
                pass
            else:
                data[attr] = val
        try: data.pop("bannedChampions")
        except: pass
        try: data.pop("participants")
        except: pass
        try: data.pop("observers")
        except: pass
        return data

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)


class FeaturedGames(PyotCore):
    games: List[FeaturedGameData]
    refresh_interval: int

    class Meta(PyotCore.Meta):
        rules = {"spectator-v4-featured-games": []}
        renamed = {"client_refresh_interval": "refresh_interval", "game_list": "games"}

    def __getattribute__(self, name):
        if name == "refresh_interval":
            return timedelta(seconds=super().__getattribute__(name))
        return super().__getattribute__(name)

    def __init__(self, platform: str = None):
        self._lazy_set(locals())

    async def _transform(self, data_):
        data = copy.deepcopy(data_)
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
                            p.pop("teamId")
                            data["gameList"][i]["teams"][0]["participants"].append(p)
                        elif p["teamId"] == 200:
                            p.pop("teamId")
                            data["gameList"][i]["teams"][1]["participants"].append(p)
                        else:
                            raise RuntimeError
                elif attr == "observers":
                    data["gameList"][i]["observersKey"] = val["encryptionKey"]
                elif attr == "teams":
                    pass
                else:
                    data["gameList"][i][attr] = val
            try: data["gameList"][i].pop("bannedChampions")
            except: pass
            try: data["gameList"][i].pop("participants")
            except: pass
            try: data["gameList"][i].pop("observers")
            except: pass
        return data
