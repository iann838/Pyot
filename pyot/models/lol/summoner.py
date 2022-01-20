from datetime import datetime
from typing import TYPE_CHECKING

from pyot.conf.model import models
from .base import PyotCore

if TYPE_CHECKING:
    from .championmastery import ChampionMasteries
    from .league import SummonerLeague
    from .thirdpartycode import ThirdPartyCode
    from .clash import ClashPlayers
    from .spectator import CurrentGame
    from .profileicon import ProfileIcon
    from ..riot.account import Account
    from .match import MatchHistory


# PYOT CORE OBJECTS

class Summoner(PyotCore):
    name: str
    id: str
    account_id: str
    level: int
    puuid: str
    profile_icon_id: int
    revision_date_millis: int

    class Meta(PyotCore.Meta):
        rules = {
            "summoner_v4_by_puuid": ["puuid"],
            "summoner_v4_by_id": ["id"],
            "summoner_v4_by_account_id": ["account_id"],
            "summoner_v4_by_name": ["name"],
        }
        renamed = {"summoner_level": "level", "revision_date": "revision_date_millis"}

    def __init__(self, id: str = None, account_id: str = None, name: str = None, puuid: str = None, platform: str = models.lol.DEFAULT_PLATFORM):
        self.initialize(locals())

    @property
    def revision_date(self) -> datetime:
        return datetime.fromtimestamp(self.revision_date_millis//1000)

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
        return ProfileIcon(id=self.profile_icon_id)

    @property
    def account(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.puuid).pipeline(self.metapipeline.name)

    @property
    def match_history(self) -> "MatchHistory":
        from .match import MatchHistory
        return MatchHistory(puuid=self.puuid, region=self.region)
