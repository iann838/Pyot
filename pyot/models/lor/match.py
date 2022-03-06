from datetime import datetime
from typing import List, Iterator, TYPE_CHECKING

from dateutil.parser import parse

from pyot.conf.model import models
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from ..riot.account import Account
    from .card import Deck


## PYOT STATIC OBJECTS

class MatchMetaData(PyotStatic):
    data_version: str
    match_id: str
    participant_puuids: List[str]

    class Meta(PyotStatic.Meta):
        raws = {"participant_puuids"}
        renamed = {"participants": "participant_puuids"}

    @property
    def participants(self) -> List["Account"]:
        from pyot.models.riot import Account
        return [Account(puuid=puuid).pipeline(self.metapipeline.name) for puuid in self.participant_puuids]


class MatchPlayerData(PyotStatic):
    puuid: str
    deck_id: str
    deck_code: str
    factions: List[str]
    game_outcome: str
    order_of_play: int
    win: bool

    class Meta(PyotStatic.Meta):
        raws = {"factions"}

    @property
    def account(self) -> "Account":
        from pyot.models.riot import Account
        return Account(puuid=self.puuid).pipeline(self.metapipeline.name)

    @property
    def deck(self) -> "Deck":
        from .card import Deck
        return Deck(code=self.deck_code)


class MatchInfoData(PyotStatic):
    mode: str # (Legal values: Constructed, Expeditions, Tutorial)
    type: str # (Legal values: Ranked, Normal, AI, Tutorial, VanillaTrial, Singleton, StandardGauntlet)
    start_time_strftime: str
    version: str
    players: List[MatchPlayerData]
    total_turn_count: int

    class Meta(PyotStatic.Meta):
        renamed = {"game_mode": "mode", "game_type": "type", "game_start_time_utc": "start_time_strftime", "game_version": "version"}

    @property
    def start_time(self) -> datetime:
        return parse(self.start_time_strftime)


## PYOT CORE OBJECTS

class Match(PyotCore):
    id: str
    metadata: MatchMetaData
    info: MatchInfoData

    class Meta(PyotCore.Meta):
        rules = {"match_v1_match": ["id"]}

    def __init__(self, id: str = None, region: str = models.lor.DEFAULT_REGION):
        self.initialize(locals())

    def transform(self, data):
        for player in data["info"]["players"]:
            if player["game_outcome"] == "win":
                player["win"] = True
            elif player["game_outcome"] == "loss":
                player["win"] = False
            else:
                player["win"] = None
        return data


class MatchHistory(PyotCore):
    ids: List[str]
    puuid: str

    class Meta(PyotCore.Meta):
        raws = {"ids"}
        rules = {"match_v1_matchlist": ["puuid"]}

    def __init__(self, puuid: str = None, region: str = models.lor.DEFAULT_REGION):
        self.initialize(locals())

    def transform(self, data):
        return {"ids": data}

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.matches[item]

    def __iter__(self) -> Iterator[Match]:
        return iter(self.matches)

    def __len__(self):
        return len(self.ids)

    @property
    def matches(self) -> List[Match]:
        return [Match(id=id_, region=self.region) for id_ in self.ids]

    @property
    def account(self) -> "Account":
        from pyot.models.riot import Account
        return Account(puuid=self.puuid).pipeline(self.metapipeline.name)
