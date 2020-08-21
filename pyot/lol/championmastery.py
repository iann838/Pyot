from .__core__ import PyotCore, PyotStatic
from datetime import datetime
from typing import List


# PYOT STATIC OBJECTS

class ChampionMasteryData(PyotStatic):
    champion_id: int
    champion_level: int
    champion_points: int
    last_play_time: datetime
    champion_points_since_last_level: int
    champion_points_until_next_level: int
    chest_granted: bool
    tokens_earned: int
    summoner_id: str

    def __getattribute__(self, name):
        if name == "last_play_time":
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        return super().__getattribute__(name)

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)


# PYOT CORE OBJECTS

class ChampionMasteries(PyotCore):
    summoner_id: str
    masteries: List[ChampionMasteryData]
    total_score: int

    class Meta(PyotCore.Meta):
        rules = {"champion-mastery-v4-all-mastery": ["summoner_id"]}

    def __init__(self, summoner_id: str = None, platform: str = None):
        self._lazy_set(locals())

    async def _transform(self, data):
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


class ChampionMastery(ChampionMasteryData, PyotCore):
    champion_id: int
    
    class Meta(PyotCore.Meta):
        rules = {"champion-mastery-v4-by-champion-id": ["summoner_id", "champion_id"]}

    def __init__(self, summoner_id: str = None, champion_id: int = None, platform: str = None):
        self._lazy_set(locals())

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)
