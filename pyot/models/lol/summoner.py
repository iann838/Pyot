from .__core__ import PyotCore
from datetime import datetime


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
            "summoner_v4_by_id": ["id"],
            "summoner_v4_by_account_id": ["account_id"],
            "summoner_v4_by_puuid": ["puuid"],
            "summoner_v4_by_name": ["name"],
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

    @property
    def profile_icon(self) -> "ProfileIcon":
        from .profileicon import ProfileIcon
        return ProfileIcon(id=self.profile_icon_id, locale=self.to_locale(self.platform))

    @property
    def account(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.puuid, region=self.region).set_pipeline("lol")

    @property
    def match_history(self) -> "MatchHistory":
        from .match import MatchHistory
        return MatchHistory(account_id=self.account_id, platform=self.platform)
