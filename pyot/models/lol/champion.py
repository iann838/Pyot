from typing import List, Dict, Iterator

from pyot.utils.champion import champion_id_by_key, champion_id_by_name
from pyot.utils.cdragon import cdragon_url, cdragon_sanitize
from pyot.core.functional import lazy_property
from .__core__ import PyotCore, PyotStatic


# PYOT STATIC OBJECTS

class ChampionTacticalData(PyotStatic):
    style: int
    difficulty: int
    damage_type: str


class ChampionPlayerStyleData(PyotStatic):
    damage: int
    durability: int
    crowd_control: int
    mobility: int
    utility: int


class ChampionChromaDescriptionsData(PyotStatic):
    region: str
    description: str


class ChampionChromaRaritiesData(PyotStatic):
    region: str
    description: str


class ChampionSkinChromaData(PyotStatic):
    id: int
    name: str
    chroma_path: str
    colors: List[str]
    descriptions: List[ChampionChromaDescriptionsData]
    rarities: List[ChampionChromaRaritiesData]

    class Meta(PyotStatic.Meta):
        raws = ["colors"]

    @lazy_property
    def chroma_abspath(self) -> str:
        return cdragon_url(self.chroma_path)


class ChampionSkinData(PyotStatic):
    id: int
    is_base: bool
    name: str
    splash_path: str
    uncentered_splash_path: str
    tile_path: str
    load_screen_path: str
    load_screen_vintage_path: str
    skin_type: str
    rarity: str
    is_legacy: bool
    chroma_path: str
    chromas: List[ChampionSkinChromaData]
    skin_line: int
    description: str
    splash_video_path: str
    collection_splash_video_path: str
    features_text: str
    region_rarity_id: int
    rarity_gem_path: str

    class Meta(PyotStatic.Meta):
        raws = ["emblems"]
        renamed = {"skin_lines": "skin_line"}

    @lazy_property
    def splash_abspath(self) -> str:
        return cdragon_url(self.splash_path)

    @lazy_property
    def uncentered_splash_abspath(self) -> str:
        return cdragon_url(self.uncentered_splash_path)

    @lazy_property
    def tile_abspath(self) -> str:
        return cdragon_url(self.tile_path)

    @lazy_property
    def load_screen_abspath(self) -> str:
        return cdragon_url(self.load_screen_path)

    @lazy_property
    def load_screen_vintage_abspath(self) -> str:
        return cdragon_url(self.load_screen_vintage_path)

    @lazy_property
    def chroma_abspath(self) -> str:
        return cdragon_url(self.chroma_path)

    @lazy_property
    def splash_video_abspath(self) -> str:
        return cdragon_url(self.splash_video_path)

    @lazy_property
    def collection_splash_video_abspath(self) -> str:
        return cdragon_url(self.collection_splash_video_path)


class ChampionPassiveData(PyotStatic):
    name: str
    icon_path: str
    description: str
    ability_video_path: str
    ability_video_image_path: str

    class Meta(PyotStatic.Meta):
        renamed = {"ability_icon_path": "icon_path"}

    @lazy_property
    def icon_abspath(self) -> str:
        return cdragon_url(self.icon_path)


class ChampionSpellData(PyotStatic):
    key: str
    name: str
    icon_path: str
    cost: List[int]
    cooldown: List[int]
    range: List[int]
    description: str
    long_description: str
    ability_video_path: str
    ability_video_image_path: str
    max_level: int
    formulas: Dict
    coefficients: Dict[str, int]
    effect_amounts: Dict[str, List[int]]
    ammo: Dict[str, List[int]]

    class Meta(PyotStatic.Meta):
        raws = {"cost", "cooldown", "range", "formulas", "coefficients", "effect_amounts", "ammo"}
        renamed = {"spell_key": "key", "ability_icon_path": "icon_path", "dynamic_description": "long_description"}

    @lazy_property
    def icon_abspath(self) -> str:
        return cdragon_url(self.icon_path)

    @lazy_property
    def cleaned_description(self) -> str:
        return cdragon_sanitize(self.long_description)


class ChampionAbilityData(PyotStatic):
    p: ChampionPassiveData
    q: ChampionSpellData
    w: ChampionSpellData
    e: ChampionSpellData
    r: ChampionSpellData


# PYOT CORE OBJECTS

class Champion(PyotCore):
    id: int
    key: str
    name: str
    lore: str
    tactical_info: ChampionTacticalData
    play_style: ChampionPlayerStyleData
    square_path: str
    stinger_sfx_path: str
    choose_vo_path: str
    ban_vo_path: str
    roles: List[str]
    skins: List[ChampionSkinData]
    abilities: ChampionAbilityData
    passive: ChampionPassiveData
    recommended_item_defaults: List[str]

    class Meta(PyotCore.Meta):
        rules = {
            "cdragon_champion_by_id": ["id"],
        }
        raws = ["roles", "recommended_item_defaults"]
        renamed = {"alias": "key", "short_bio": "lore", "playstyle_info": "play_style", "square_portrait_path": "square_path", "spells": "abilities"}

    def __init__(self, id: int = None, key: str = None, name: str = None, locale: str = None):
        self._lazy_set(locals())

    async def _setup(self):
        if not hasattr(self, "id"):
            if hasattr(self, "key"):
                self.id = await champion_id_by_key(self.key)
            elif hasattr(self, "name"):
                self.id = await champion_id_by_name(self.name)

    def _clean(self):
        if self.locale.lower() == "en_us":
            self._meta.server = "default"

    def _transform(self, data):
        for skin in data["skins"]:
            if skin["skinLines"] is not None:
                skin["skinLines"] = skin["skinLines"][0]["id"]
        spells = {}
        for spell in data["spells"]:
            spell["cost"] = spell.pop("costCoefficients")[:5]
            spell["cooldown"] = spell.pop("cooldownCoefficients")[:5]
            spells[spell["spellKey"]] = spell
        data["spells"] = spells
        return data

    @lazy_property
    def square_abspath(self) -> str:
        return cdragon_url(self.square_path)

    @lazy_property
    def stinger_sfx_abspath(self) -> str:
        return cdragon_url(self.stinger_sfx_path)

    @lazy_property
    def choose_vo_abspath(self) -> str:
        return cdragon_url(self.choose_vo_path)

    @lazy_property
    def ban_vo_abspath(self) -> str:
        return cdragon_url(self.ban_vo_path)

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.id)


class Champions(PyotCore):
    champions: List[Champion]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_champion_summary": []}

    def __init__(self, locale: str = None):
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
        if self.locale.lower() == "en_us":
            self._meta.server = "default"

    def _transform(self, data):
        return {"champions": data}
