from typing import List, Iterator, TYPE_CHECKING
from datetime import datetime, timedelta

from pyot.conf.model import models
from pyot.core.functional import parse_camelcase
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from .summoner import Summoner
    from .champion import Champion
    from .item import Item
    from .trait import Trait


# PYOT STATIC OBJECTS

class MatchMetadataData(PyotStatic):
    id: str
    data_version: str
    participant_puuids: List[str]

    class Meta(PyotStatic.Meta):
        raws = {"participant_puuids"}
        renamed = {"match_id": "id", "participants": "participant_puuids"}

    @property
    def participants(self) -> List["Summoner"]:
        from .summoner import Summoner
        return [Summoner(puuid=i, platform=self.id.split('_')[0]) for i in self.participant_puuids]


class MatchInfoCompanionData(PyotStatic):
    content_id: str
    skin_id: int
    species: str


class MatchInfoTraitData(PyotStatic):
    name: str
    num_units: int
    style: int
    tier_current: int
    tier_total: int

    @property
    def trait(self) -> "Trait":
        from .trait import Trait
        return Trait(key=self.name)


class MatchInfoUnitData(PyotStatic):
    item_ids: List[int]
    champion_key: str
    chosen: str
    name: str
    rarity: int
    tier: int

    class Meta(PyotStatic.Meta):
        raws = {"item_ids"}
        renamed = {"items": "item_ids", "character_id": "champion_key"}

    @property
    def items(self) -> List["Item"]:
        from .item import Item
        return [Item(id=i) for i in self.item_ids]

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(key=self.champion_key)


class MatchInfoParticipantData(PyotStatic):
    companion: MatchInfoCompanionData
    gold_left: int
    last_round: int
    level: int
    placement: int
    players_eliminated: int
    puuid: str
    time_eliminated_secs: float
    total_damage_to_players: int
    traits: List[MatchInfoTraitData]
    units: List[MatchInfoUnitData]
    _pyot_calculated_platform: str

    class Meta(PyotStatic.Meta):
        renamed = {"time_eliminated": "time_eliminated_secs"}

    @property
    def time_eliminated(self) -> timedelta:
        return timedelta(seconds=self.time_eliminated_secs)

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(puuid=self.puuid, platform=self._pyot_calculated_platform)


class MatchInfoData(PyotStatic):
    datetime_millis: int
    length_secs: float
    variation: str
    version: str
    participants: List[MatchInfoParticipantData]
    queue_id: int
    tft_mode: str
    tft_set_number: int

    class Meta(PyotStatic.Meta):
        renamed = {"game_datetime": "datetime_millis", "game_length": "length_secs", "game_variation": "variation", "game_version": "version"}

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.datetime_millis//1000)

    @property
    def length(self) -> timedelta:
        return timedelta(seconds=self.length_secs)


# PYOT CORE OBJECTS

class Match(PyotCore):
    id: str
    info: MatchInfoData
    metadata: MatchMetadataData

    class Meta(PyotCore.Meta):
        rules = {"match_v1_match": ["id"]}

    def __init__(self, id: str = None, region: str = models.tft.DEFAULT_REGION):
        self.initialize(locals())

    def transform(self, data):
        platform = self.id.split("_")[0]
        for i in range(len(data["info"]["participants"])):
            data["info"]["participants"][i]["_pyot_calculated_platform"] = platform
        return data


class MatchHistory(PyotCore):
    ids: List[str]
    puuid: str

    class Meta(PyotCore.Meta):
        rules = {"match_v1_matchlist": ["puuid"]}
        raws = {"ids"}

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return Match(id=self.ids[item], region=self.region)

    def __iter__(self) -> Iterator[Match]:
        return iter(self.matches)

    def __len__(self):
        return len(self.ids)

    def __init__(self, puuid: str = None, region: str = models.tft.DEFAULT_REGION):
        self.initialize(locals())

    def query(self, count: int = 20):
        '''Query parameters setter.'''
        self._meta.query = parse_camelcase(locals())
        return self

    @property
    def matches(self) -> List[Match]:
        return [Match(id=id_, region=self.region) for id_ in self.ids]

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        try:
            return Summoner(account_id=self.account_id, platform=self.ids[0].split("_")[0])
        except (AttributeError, IndexError) as e:
            raise AttributeError("Match history is empty, could not identify platform from list") from e

    def transform(self, data):
        return {"ids": data}
