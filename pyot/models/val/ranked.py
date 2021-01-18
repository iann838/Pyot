from typing import List, Iterator
from .__core__ import PyotCore, PyotStatic

# PYOT STATIC OBJECTS

class LeaderboardPlayerData(PyotStatic):
    puuid: str
    game_name: str
    tag_line: str
    leaderboard_rank: int
    ranked_rating: int
    number_of_wins: int

    @property
    def account(self) -> "Account":
        from ..riot.account import Account
        return Account(puuid=self.puuid, region=self.region).set_pipeline("val")


# PYOT CORE OBJECTS

class Leaderboard(PyotCore):
    act_id: str
    total_players: int
    players: List[LeaderboardPlayerData]
    shard: str

    class Meta(PyotCore.Meta):
        rules = {"ranked_v1_leaderboards": ["act_id"]}

    def __init__(self, act_id: str = None, platform: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.players[item]

    def __iter__(self) -> Iterator[LeaderboardPlayerData]:
        return iter(self.players)

    def __len__(self) -> int:
        return len(self.players)

    def query(self, size: int = None, start_index: int = None):
        '''Add query parameters to the object.'''
        self._meta.query = self._parse_camel(locals())
        return self
