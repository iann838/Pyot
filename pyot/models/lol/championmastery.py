from .__core__ import PyotCore, PyotStatic
from datetime import datetime
from typing import List, Iterator


# PYOT CORE OBJECTS

class ChampionMastery(PyotCore):
    champion_id: int
    champion_level: int
    champion_points: int
    last_play_time: datetime
    champion_points_since_last_level: int
    champion_points_until_next_level: int
    chest_granted: bool
    tokens_earned: int
    summoner_id: str
    
    class Meta(PyotCore.Meta):
        rules = {"champion_mastery_v4_by_champion_id": ["summoner_id", "champion_id"]}

    def __getattribute__(self, name):
        if name == "last_play_time":
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        return super().__getattribute__(name)

    def __init__(self, summoner_id: str = None, champion_id: int = None, platform: str = None):
        self._lazy_set(locals())

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.champion_id, locale=self.to_locale(self.platform))

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.champion_id)



class ChampionMasteries(PyotCore):
    summoner_id: str
    masteries: List[ChampionMastery]
    total_score: int

    class Meta(PyotCore.Meta):
        rules = {"champion_mastery_v4_all_mastery": ["summoner_id"]}

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.masteries[item]

    def __iter__(self) -> Iterator[ChampionMastery]:
        return iter(self.masteries)

    def __len__(self):
        return len(self.masteries)

    def __init__(self, summoner_id: str = None, platform: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        new_data = {}
        new_data["totalScore"] = 0
        for a in data:
            new_data["totalScore"] += a["championLevel"]
        new_data["masteries"] = data
        return new_data

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)
