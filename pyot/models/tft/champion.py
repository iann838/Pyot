from typing import List, Iterator

from pyot.utils.cdragon import tft_champ_sanitize, tft_url
from pyot.utils.champion import champion_key_by_id, champion_key_by_name
from pyot.core.functional import lazy_property, cache_indexes
from pyot.core.exceptions import NotFound
from .__core__ import PyotCore, PyotStatic


# PYOT STATIC OBJECTS

class ChampionAbilityVariableData(PyotStatic):
    name: str
    value: List[int]

    class Meta(PyotStatic.Meta):
        raws = ["value"]


class ChampionAbilityData(PyotStatic):
    name: str
    description: str
    icon_path: str
    variables: List[ChampionAbilityVariableData]

    class Meta(PyotStatic.Meta):
        renamed = {"desc": "description", "icon": "icon_path"}

    @lazy_property
    def icon_abspath(self) -> str:
        return tft_url(self.icon_path)

    @lazy_property
    def cleaned_description(self, data):
        return tft_champ_sanitize(self.description, self["variables"])


class ChampionStatData(PyotStatic):
    armor: int
    attack_speed: float
    crit_chance: float
    crit_multiplier: float
    damage: int
    hp: int
    initial_mana: int
    magic_resist: int
    mana: int
    range: int


# PYOT CORE OBJECTS

class Champion(PyotCore):
    set: str
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
        rules = {"cdragon_tft_full": ["key", "set"]}
        renamed = {"api_name": "key", "traits": "trait_keys", "icon": "icon_path"}

    def __init__(self, key: str = None, set: int = None, lol_id: int = None, name: str = None, locale: str = None):
        a = locals()
        if key and not set:
            try:
                a["set"] = int(key.split("_")[0][-1])
            except Exception:
                raise TypeError("Could not parse 'set' value from key")
        self._lazy_set(a)

    @cache_indexes
    def _filter(self, indexer, data):
        return indexer.get(self.key, data["sets"][str(self.set)]["champions"], "apiName")

    async def _setup(self):
        if not hasattr(self, "key"):
            if hasattr(self, "lol_id"):
                key = await champion_key_by_id(self.lol_id)
                self.key = f"TFT{self.set}_{key}"
            elif hasattr(self, "name"):
                key = await champion_key_by_name(self.name)
                self.key = f"TFT{self.set}_{key}"

    def _clean(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"
        self._hide_load_value("key")
    @lazy_property
    def icon_abspath(self) -> str:
        return tft_url(self.icon_path)

    @property
    def traits(self) -> List["Trait"]:
        from .trait import Trait
        return [Trait(key=i, locale=self.locale) for i in self.trait_keys]


class Champions(PyotCore):
    set: int
    champions: List[Champion]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["set"]}

    def __init__(self, set: int = None, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.champions[item]

    def __iter__(self) -> Iterator[Champion]:
        return iter(self.champions)

    def __len__(self):
        return len(self.champions)

    def _clean(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"

    def _filter(self, data):
        try:
            return data["sets"][str(self.set)]["champions"]
        except KeyError:
            raise NotFound("Request was successful but filtering gave no matching item")

    def _transform(self, data):
        return {"champions": data}
