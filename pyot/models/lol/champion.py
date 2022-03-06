from typing import List, Dict, Iterator, TYPE_CHECKING

from pyot.conf.model import models
from pyot.core.functional import lazy_property
from pyot.utils.lol.champion import id_by_key, id_by_name
from pyot.utils.lol.cdragon import abs_url, sanitize
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from .merakichampion import MerakiChampion


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
    region: str = None
    description: str


class ChampionChromaRaritiesData(PyotStatic):
    region: str = None
    description: str
    rarity: int


class ChampionSkinChromaData(PyotStatic):
    id: int
    name: str
    chroma_path: str
    colors: List[str]
    descriptions: List[ChampionChromaDescriptionsData]
    rarities: List[ChampionChromaRaritiesData]

    class Meta(PyotStatic.Meta):
        raws = {"colors"}

    @lazy_property
    def chroma_abspath(self) -> str:
        return abs_url(self.chroma_path, self.metaroot.version)


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
    emblems: List[str]
    skin_line: int
    description: str
    splash_video_path: str
    collection_splash_video_path: str
    features_text: str
    region_rarity_id: int
    rarity_gem_path: str

    class Meta(PyotStatic.Meta):
        raws = {"emblems"}
        renamed = {"skin_lines": "skin_line"}

    @lazy_property
    def splash_abspath(self) -> str:
        return abs_url(self.splash_path, self.metaroot.version)

    @lazy_property
    def uncentered_splash_abspath(self) -> str:
        return abs_url(self.uncentered_splash_path, self.metaroot.version)

    @lazy_property
    def tile_abspath(self) -> str:
        return abs_url(self.tile_path, self.metaroot.version)

    @lazy_property
    def load_screen_abspath(self) -> str:
        return abs_url(self.load_screen_path, self.metaroot.version)

    @lazy_property
    def load_screen_vintage_abspath(self) -> str:
        return abs_url(self.load_screen_vintage_path, self.metaroot.version)

    @lazy_property
    def chroma_abspath(self) -> str:
        return abs_url(self.chroma_path, self.metaroot.version)

    @lazy_property
    def splash_video_abspath(self) -> str:
        return abs_url(self.splash_video_path, self.metaroot.version)

    @lazy_property
    def collection_splash_video_abspath(self) -> str:
        return abs_url(self.collection_splash_video_path, self.metaroot.version)


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
        return abs_url(self.icon_path, self.metaroot.version)


class ChampionSpellData(PyotStatic):
    key: str
    name: str
    icon_path: str
    cost: List[float]
    cooldown: List[float]
    range: List[float]
    description: str
    long_description: str
    ability_video_path: str
    ability_video_image_path: str
    max_level: int
    formulas: Dict
    coefficients: Dict[str, float]
    effect_amounts: Dict[str, List[float]]
    ammo: Dict[str, List[float]]

    class Meta(PyotStatic.Meta):
        raws = {"cost", "cooldown", "range", "formulas", "coefficients", "effect_amounts", "ammo"}
        renamed = {"spell_key": "key", "ability_icon_path": "icon_path", "dynamic_description": "long_description"}

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)

    @lazy_property
    def cleaned_description(self) -> str:
        return sanitize(self.long_description)


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
    title: str
    recommended_item_defaults: List[str]

    class Meta(PyotCore.Meta):
        rules = {
            "cdragon_champion_by_id": ["version", "locale", "id"],
        }
        raws = {"roles", "recommended_item_defaults"}
        renamed = {"alias": "key", "short_bio": "lore", "playstyle_info": "play_style", "square_portrait_path": "square_path", "spells": "abilities"}

    def __init__(self, id: int = None, key: str = None, name: str = None, version: str = models.lol.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    async def setup(self):
        if not hasattr(self, "id"):
            if hasattr(self, "key"):
                self.id = await id_by_key(self.key)
            elif hasattr(self, "name"):
                self.id = await id_by_name(self.name)

    def transform(self, data):
        if not data.get("skins", None):
            return data
        for skin in data["skins"]:
            if skin["skinLines"] is not None:
                skin["skinLines"] = skin["skinLines"][0]["id"]
        spells = {}
        for spell in data["spells"]:
            spell["cost"] = spell.pop("costCoefficients")
            spell["cooldown"] = spell.pop("cooldownCoefficients")
            spells[spell["spellKey"]] = spell
        spells["p"] = data["passive"].copy()
        data["spells"] = spells
        return data

    @lazy_property
    def square_abspath(self) -> str:
        return abs_url(self.square_path, self.metaroot.version)

    @lazy_property
    def stinger_sfx_abspath(self) -> str:
        return abs_url(self.stinger_sfx_path, self.metaroot.version)

    @lazy_property
    def choose_vo_abspath(self) -> str:
        return abs_url(self.choose_vo_path, self.metaroot.version)

    @lazy_property
    def ban_vo_abspath(self) -> str:
        return abs_url(self.ban_vo_path, self.metaroot.version)

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.id)


class Champions(PyotCore):
    champions: List[Champion]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_champion_summary": ["version", "locale"]}

    def __init__(self, version: str = models.lol.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.champions[item]

    def __iter__(self) -> Iterator[Champion]:
        return iter(self.champions)

    def __len__(self):
        return len(self.champions)

    def transform(self, data):
        return {"champions": data}
