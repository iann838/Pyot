from typing import List, Iterator, TYPE_CHECKING

from pyot.conf.model import models
from pyot.core.functional import lazy_property, cache_indexes
from pyot.core.exceptions import NotFound
from pyot.utils.tft.cdragon import join_set_data, sanitize_champion, abs_url
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from .trait import Trait


# PYOT STATIC OBJECTS

class ChampionAbilityVariableData(PyotStatic):
    name: str
    value: List[float]

    class Meta(PyotStatic.Meta):
        raws = {"value"}


class ChampionAbilityData(PyotStatic):
    name: str
    description: str
    icon_path: str
    variables: List[ChampionAbilityVariableData]

    class Meta(PyotStatic.Meta):
        renamed = {"desc": "description", "icon": "icon_path"}

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)

    @lazy_property
    def cleaned_description(self) -> str:
        return sanitize_champion(self.description, self["variables"])


class ChampionStatData(PyotStatic):
    armor: float
    attack_speed: float
    crit_chance: float
    crit_multiplier: float
    damage: float
    hp: float
    initial_mana: float
    magic_resist: float
    mana: float
    range: float


# PYOT CORE OBJECTS

class Champion(PyotCore):
    set: int
    key: str
    name: str
    cost: int
    stats: ChampionStatData
    trait_keys: List[str]
    ability: ChampionAbilityData
    lol_id: int
    icon_path: str

    class Meta(PyotCore.Meta):
        raws = {"trait_keys"}
        rules = {"cdragon_tft_full": ["?key", "?set", "version", "locale"]}
        renamed = {"api_name": "key", "traits": "trait_keys", "icon": "icon_path"}

    def __init__(self, key: str = None, set: int = None, version: str = models.tft.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())
        if key and set is None:
            self.find_set()

    def find_set(self):
        try:
            self.set = int(self.key.split("_")[0][3:])
        except Exception:
            self.set = -1

    @cache_indexes
    def filter(self, indexer, data):
        return indexer.get(
            self.key,
            join_set_data(data, self.set, "champions"),
            "apiName"
        )

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)

    @property
    def traits(self) -> List["Trait"]:
        from .trait import Trait
        return [Trait(key=i, set=self.set, version=self.version, locale=self.locale) for i in self.trait_keys]


class Champions(PyotCore):
    set: int
    champions: List[Champion]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["?set", "version", "locale"]}

    def __init__(self, set: int = -1, version: str = models.tft.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.champions[item]

    def __iter__(self) -> Iterator[Champion]:
        return iter(self.champions)

    def __len__(self):
        return len(self.champions)

    def filter(self, data):
        try:
            return join_set_data(data, self.set, "champions")
        except KeyError as e:
            raise NotFound("Request was successful but filtering gave no matching item") from e

    def transform(self, data):
        return {"champions": data}
