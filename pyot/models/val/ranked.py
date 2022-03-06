from typing import Dict, List, Iterator, TYPE_CHECKING

from pyot.conf.model import models
from pyot.core.functional import parse_camelcase
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from ..riot.account import Account


# PYOT STATIC OBJECTS

class LeaderboardPlayerData(PyotStatic):
    puuid: str
    game_name: str
    tag_line: str
    leaderboard_rank: int
    ranked_rating: int
    number_of_wins: int
    competitive_tier: int

    @property
    def account(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.puuid).pipeline(self.metapipeline.name)


class LeaderboardTierDetailData(PyotStatic):
    ranked_rating_threshold: int
    starting_page: int
    starting_index: int


# PYOT CORE OBJECTS

class Leaderboard(PyotCore):
    act_id: str
    total_players: int
    players: List[LeaderboardPlayerData]
    immortal_starting_page: int
    immortal_starting_index: int
    top_tier_rr_threshold: int
    tier_details: Dict[str, LeaderboardTierDetailData]
    start_index: int
    query_str: str
    shard: str

    class Meta(PyotCore.Meta):
        rules = {"ranked_v1_leaderboards": ["act_id"]}
        renamed = {"query": "query_str"}

    def __init__(self, act_id: str = None, platform: str = models.val.DEFAULT_PLATFORM):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.players[item]

    def __iter__(self) -> Iterator[LeaderboardPlayerData]:
        return iter(self.players)

    def __len__(self) -> int:
        return len(self.players)

    def query(self, size: int = None, start_index: int = None):
        '''Query parameters setter.'''
        self._meta.query = parse_camelcase(locals())
        return self
