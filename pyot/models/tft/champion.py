from .__core__ import PyotCore, PyotStatic
from ...stores.cdragon import CDragon, CDragonTransformers
from ...core.exceptions import NotFound
from typing import List, Iterator


# PYOT STATIC OBJECTS

class ChampionAbilityVariableData(PyotStatic):
    name: str
    value: List[int]

    class Meta(PyotStatic.Meta):
        raws = ["value"]


class ChampionAbilityData(PyotStatic):
    name: str
    description: str
    cleaned_description: str
    icon_path: str
    variables: List[ChampionAbilityVariableData]

    class Meta(PyotStatic.Meta):
        renamed = {"desc": "description"}


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
        renamed = {"api_name": "key", "traits": "trait_keys"}

    def __init__(self, key: str = None, set: int = None, lol_id: int = None, name: str = None, locale: str = None):
        a = locals()
        if key and not set:
            try:
                a["set"] = int(key.split("_")[0][-1])
            except Exception:
                raise RuntimeError("Could not parse 'set' value from key")
        self._lazy_set(a)

    def filter(self, data_):
        try:
            data = data_["sets"][str(self.set)]["champions"]
        except KeyError:
            raise NotFound
        for item in data:
            if item["apiName"] == self.key:
                return item
        raise NotFound
    
    async def _clean(self):
        if not hasattr(self, "key"):
            if hasattr(self, "lol_id"):
                key = await self.Meta.pipeline.transform_key(CDragon, list(self.Meta.rules.keys())[0], "lol_id", self.lol_id)
                self.key = f"TFT{self.set}_{key}"
            elif hasattr(self, "name"):
                key = await self.Meta.pipeline.transform_key(CDragon, list(self.Meta.rules.keys())[0], "name", self.name)
                self.key = f"TFT{self.set}_{key}"

    async def _refactor(self):
        if self.locale.lower() == "default":
            self.Meta.server = "en_us"
        load = getattr(self.Meta, "load")
        load.pop("key")

    async def _transform(self, data):
        tr = CDragonTransformers(self.locale)
        data["iconPath"] = tr.tft_url_assets(data.pop("icon"))
        data["ability"]["cleanedDescription"] = tr.tft_champ_sanitize(data["ability"]["desc"], data["ability"]["variables"])
        data["ability"]["iconPath"] = tr.tft_url_assets(data["ability"].pop("icon"))
        return data

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
        return self.champions[item]

    def __iter__(self) -> Iterator[Champion]:
        return iter(self.champions)

    async def _refactor(self):
        if self.locale.lower() == "default":
            self.Meta.server = "en_us"

    def filter(self, data_):
        try:
            data = data_["sets"][str(self.set)]["champions"]
        except KeyError:
            raise NotFound
        return data

    async def _transform(self, data_):
        tr = CDragonTransformers(self.locale)
        champions = []
        for data in data_:
            data["iconPath"] = tr.tft_url_assets(data.pop("icon"))
            data["ability"]["cleanedDescription"] = tr.tft_champ_sanitize(data["ability"]["desc"], data["ability"]["variables"])
            data["ability"]["iconPath"] = tr.tft_url_assets(data["ability"].pop("icon"))
            champions.append({"data": data})
        return {"champions": champions}