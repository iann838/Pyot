from .__core__ import PyotCore, PyotStatic
from ...stores.cdragon import CDragon, CDragonTransformers
from typing import Any, List


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


class ChampionSkinData(PyotStatic):
    id: int
    is_base: bool
    name: str
    splash_path: str
    uncentered_splash_path: str
    tile_path: str
    load_screen_path: str
    skin_type: str
    rarity: str
    is_legacy: bool
    chroma_path: str
    chromas: List[ChampionSkinChromaData]
    skin_line: int
    description: str

    class Meta(PyotStatic.Meta):  # Emblems are removed as its only available to China TENCENT
        removed = ["splash_video_path", "features_text", "rarity_gem_path", "region_rarity_id", "load_screen_vintage_path", "emblems"]
        renamed = {"skin_lines": "skin_line"}


class ChampionPassiveData(PyotStatic):
    name: str
    icon_path: str
    description: str

    class Meta(PyotStatic.Meta):
        removed = ["ability_video_path", "ability_video_image_path"]
        renamed = {"ability_icon_path": "icon_path"}


class ChampionSpellData(PyotStatic):
    key: str
    name: str
    icon_path: str
    cost: List[int]
    cooldown: List[int]
    range: List[int]
    description: str
    long_description: str
    cleaned_description: str

    class Meta(PyotStatic.Meta):
        raws = ["cost", "cooldown", "range"]
        removed = ["ability_video_path", "ability_video_image_path"]
        renamed = {"spell_key": "key", "ability_icon_path": "icon_path", "dynamic_description": "long_description"}


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
    tactical_info: ChampionTacticalData
    play_style: ChampionPlayerStyleData
    square_path: str
    roles: List[str]
    skins: List[ChampionSkinData]
    abilities: ChampionAbilityData

    class Meta(PyotCore.Meta):
        rules = {
            "cdragon_champion_by_id": ["id"],
        }
        raws = ["roles"]
        renamed = {"alias": "key", "short_bio": "lore", "playstyle_info": "play_style", "square_portrait_path": "square_path", "spells": "abilities"}
        removed = ["stinger_sfx_path", "choose_vo_path", "ban_vo_path", "recommended_item_defaults"]

    def __init__(self, id: int = None, key: str = None, name: str = None, locale: str = None):
        self._lazy_set(locals())

    async def _clean(self):
        if not hasattr(self, "id"):
            if hasattr(self, "key"):
                self.id = await self.Meta.pipeline.transform_key(CDragon, list(self.Meta.rules.keys())[0], "key", self.key)
            elif hasattr(self, "name"):
                self.id = await self.Meta.pipeline.transform_key(CDragon, list(self.Meta.rules.keys())[0], "name", self.name)

    async def _refactor(self):
        if self.locale.lower() == "en_us":
            self.Meta.server = "default"

    async def _transform(self, data):
        tr = CDragonTransformers(self.locale)
        data["squarePortraitPath"] = tr.url_assets(data["squarePortraitPath"])
        data["tacticalInfo"]["damageType"] = tr.start_k(data["tacticalInfo"]["damageType"])
        skins = []
        for skin in data["skins"]:
            skin["splashPath"] = tr.url_assets(skin["splashPath"])
            skin["uncenteredSplashPath"] = tr.url_assets(skin["uncenteredSplashPath"])
            skin["tilePath"] = tr.url_assets(skin["tilePath"])
            skin["loadScreenPath"] = tr.url_assets(skin["loadScreenPath"])
            skin["rarity"] = tr.start_k(skin["rarity"])
            skin["chromaPath"] = tr.url_assets(skin["chromaPath"])
            if "chromas" in skin:
                chromas = []
                for chroma in skin["chromas"]:
                    chroma["chromaPath"] = tr.url_assets(chroma["chromaPath"])
                    chromas.append(chroma)
                skin["chromas"] = chromas
            if skin["skinLines"] is not None:
                skin["skinLines"] = skin["skinLines"][0]["id"]
            skins.append(skin)
        data["skins"] = skins
        data["passive"]["abilityIconPath"] = tr.url_assets(data["passive"]["abilityIconPath"])
        spells = {}
        for spell in data["spells"]:
            spell["abilityIconPath"] = tr.url_assets(spell["abilityIconPath"])
            spell["cost"] = spell.pop("costCoefficients")[:5]
            spell["cooldown"] = spell.pop("cooldownCoefficients")[:5]
            spell["cleanedDescription"] = tr.sanitize(spell["dynamicDescription"])
            spell.pop("formulas", None)
            spell.pop("coefficients", None)
            spell.pop("effectAmounts", None)
            spell.pop("ammo", None)
            spell.pop("maxLevel", None)
            spells[spell["spellKey"]] = spell
        spells["p"] = data.pop("passive")
        data["spells"] = spells
        return data

    @property
    def meraki_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.id if hasattr(self,"id") else None, name=self.name if hasattr(self,"name") else None, 
            key=self.key if hasattr(self,"key") else None)
