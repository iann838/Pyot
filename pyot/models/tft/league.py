from typing import List, Iterator, NoReturn, TYPE_CHECKING

from pyot.conf.model import models
from pyot.core.functional import parse_camelcase
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from .summoner import Summoner


# PYOT STATIC OBJECTS

class MiniSeriesData(PyotStatic):
    target: int
    wins: int
    losses: int
    progress: str


class LeagueEntryData(PyotStatic):
    summoner_id: str
    summoner_name: str
    league_points: int
    rank: str
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    fresh_blood: bool
    hot_streak: bool
    mini_series: MiniSeriesData

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, name=self.summoner_name, platform=self.platform)


class SummonerLeagueEntryData(LeagueEntryData):
    league_id: str
    queue: str
    tier: str

    class Meta(LeagueEntryData.Meta):
        renamed = {"queue_type": "queue"}

    @property
    def league(self) -> "League":
        return League(id=self.league_id, platform=self.platform)


class League(PyotCore):
    tier: str
    id: str
    queue: str
    name: str
    entries: List[LeagueEntryData]

    class Meta(PyotCore.Meta):
        rules = {"league_v1_league_by_league_id": ["id"]}
        renamed = {"league_id": "id"}

    def __init__(self, id: str = None, platform: str = models.tft.DEFAULT_PLATFORM):
        self.initialize(locals())


class ApexLeague(League):
    queue: str
    id: str

    class Meta(League.Meta):
        pass

    def __init__(self, platform: str = models.tft.DEFAULT_PLATFORM):
        self.initialize(locals())

    @property
    def league(self) -> League:
        return League(id=self.id, platform=self.platform)


class ChallengerLeague(ApexLeague):

    class Meta(ApexLeague.Meta):
        rules = {"league_v1_challenger_league": []}


class GrandmasterLeague(ApexLeague):

    class Meta(ApexLeague.Meta):
        rules = {"league_v1_grandmaster_league": []}


class MasterLeague(ApexLeague):

    class Meta(ApexLeague.Meta):
        rules = {"league_v1_master_league": []}


class SummonerLeague(PyotCore):
    summoner_id: str
    entries: List[SummonerLeagueEntryData]

    class Meta(PyotCore.Meta):
        rules = {"league_v1_summoner_entries": ["summoner_id"]}

    def __init__(self, summoner_id: str = None, platform: str = models.tft.DEFAULT_PLATFORM):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.entries[item]

    def __iter__(self) -> Iterator[SummonerLeagueEntryData]:
        return iter(self.entries)

    def __len__(self):
        return len(self.entries)

    def transform(self, data):
        new_data = {}
        new_data["entries"] = data
        return new_data

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)


class DivisionLeague(SummonerLeague):
    queue: str
    division: str
    tier: str

    class Meta(SummonerLeague.Meta):
        rules = {"league_v1_entries_by_division": ["tier", "division"]}
        division_list = ["I", "II", "III", "IV"]
        tier_list = ["DIAMOND", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]

    def __init__(self, division: str = None, tier: str = None, platform: str = models.tft.DEFAULT_PLATFORM):
        self.initialize(locals())

    def query(self, page: int = None):
        '''Query parameters setter.'''
        if page == 0: raise AttributeError("Invalid 'page' attribute, it should be greater than 0")
        self._meta.query = parse_camelcase(locals())
        return self

    @property
    def summoner(self) -> NoReturn:
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'summoner'")
