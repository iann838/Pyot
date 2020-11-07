from .__core__ import PyotCore, PyotStatic
from datetime import datetime, timedelta
from typing import List, Iterator
from dateutil.parser import parse

## PYOT STATIC OBJECTS

class MatchMetaData(PyotStatic):
    data_version: str
    match_id: str
    participant_puuids: List[str]

    class Meta(PyotStatic.Meta):
        raws = ["participant_puuids"]
        renamed = {"participants": "participant_puuids"}

    @property
    def participants(self) -> List["Account"]:
        from pyot.models.riot import Account
        return [Account(puuid=puuid, region=self.region).set_pipeline("lor") for puuid in self.participant_puuids]


class MatchPlayerData(PyotStatic):
    puuid: str
    deck_id: str
    deck_code: str
    factions: List[str]
    game_outcome: str
    order_of_play: int
    win: bool

    class Meta(PyotStatic.Meta):
        raws = ["factions"]

    @property
    def account(self) -> "Account":
        from pyot.models.riot import Account
        return Account(puuid=self.puuid, region=self.region).set_pipeline("lor")

    @property
    def deck(self) -> "Deck":
        from .card import Deck
        return Deck(code=self.deck_code, locale=self.to_locale(self.region))


class MatchInfoData(PyotStatic):
    mode: str # (Legal values: Constructed, Expeditions, Tutorial)
    type: str # (Legal values: Ranked, Normal, AI, Tutorial, VanillaTrial, Singleton, StandardGauntlet)
    creation: datetime
    version: str
    players: List[MatchPlayerData]
    total_turn_count: int

    class Meta(PyotStatic.Meta):
        renamed = {"game_mode": "mode", "game_type": "type", "game_start_time_utc": "creation", "game_version": "version"}

    def __getattribute__(self, name):
        if name == "creation":
            return parse(super().__getattribute__(name))
        return super().__getattribute__(name)


## PYOT CORE OBJECTS

class Match(PyotCore):
    id: int
    metadata: MatchMetaData
    info: MatchInfoData

    class Meta(PyotCore.Meta):
        rules = {"match_v1_match": ["id"]}

    def __init__(self, id: int = None, region: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
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
    _matches: List[Match]

    class Meta(PyotCore.Meta):
        raws = ["ids"]
        rules = {"match_v1_matchlist": ["puuid"]}

    def __init__(self, puuid: str = None, region: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        return {"ids": data}

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.matches[item]

    def __iter__(self) -> Iterator[Match]:
        return iter(self.matches)

    def __len__(self):
        return len(self.matches)

    @property
    def matches(self) -> List[Match]:
        if hasattr(self, "_matches"):
            return self._matches
        self._matches = [Match(id=id_, region=self.region) for id_ in self.ids]
        return self._matches

    @property
    def account(self) -> "Account":
        from pyot.models.riot import Account
        return Account(puuid=self.puuid, region=self.region).set_pipeline("lor")
