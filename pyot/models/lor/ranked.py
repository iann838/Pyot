from .__core__ import PyotCore, PyotStatic
from typing import List, Iterator

## PYOT STATIC OBJECTS

class LeaderboardPlayerData(PyotStatic):
    name: str
    rank: int
    lp: int


# PYOT CORE OBJECTS

class Leaderboard(PyotCore):
    players: List[LeaderboardPlayerData]

    class Meta(PyotCore.Meta):
        rules = {"ranked_v1_leaderboards": []}

    def __init__(self, region: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.players[item]

    def __iter__(self) -> Iterator[LeaderboardPlayerData]:
        return iter(self.players)

    def __len__(self) -> int:
        return len(self.players)
