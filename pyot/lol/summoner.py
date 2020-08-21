from .__core__ import PyotCore
from datetime import datetime
from ..core.object import PyotLazyObject


# PYOT CORE OBJECTS

class Summoner(PyotCore):
    name: str
    id: str
    account_id: str
    level: int
    puuid: str
    profile_icon_id: int
    revision_date: datetime

    class Meta(PyotCore.Meta):
        rules = {
            "summoner-v4-by-name": ["name"],
            "summoner-v4-by-id": ["id"],
            "summoner-v4-by-account-id": ["account_id"],
            "summoner-v4-by-puuid": ["puuid"],
        }
        renamed = {"summoner_level": "level"}

    def __getattribute__(self, name):
        if name == "revision_date":
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        return super().__getattribute__(name)

    def __init__(self, id: str = None, account_id: str = None, name: str = None, puuid: str = None, platform: str = None):
        self._lazy_set(locals())

    @property
    def champion_masteries(self) -> "ChampionMasteries":
        from .championmastery import ChampionMasteries
        return ChampionMasteries(summoner_id=self.id, platform=self.platform)

    @property
    def league_entries(self) -> "SummonerLeague":
        from .league import SummonerLeague
        return SummonerLeague(summoner_id=self.id, platform=self.platform)

    @property
    def third_party_code(self) -> "ThirdPartyCode":
        from .thirdpartycode import ThirdPartyCode
        return ThirdPartyCode(summoner_id=self.id, platform=self.platform)

    @property
    def clash_players(self) -> "ClashPlayers":
        from .clash import ClashPlayers
        return ClashPlayers(summoner_id=self.id, platform=self.platform)

    @property
    def current_game(self) -> "CurrentGame":
        from .spectator import CurrentGame
        return CurrentGame(summoner_id=self.id, platform=self.platform)
