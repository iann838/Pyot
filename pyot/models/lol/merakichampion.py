from typing import List, TYPE_CHECKING, Union

from pyot.utils.lol.champion import key_by_id, key_by_name
from .base import PyotStatic, PyotCore

if TYPE_CHECKING:
    from .champion import Champion


# PYOT STATIC OBJECTS

class MerakiChampionSpellModifierData(PyotStatic):
    values: List[float]
    units: List[str]

    class Meta(PyotStatic.Meta):
        raws = {"values", "units"}


class MerakiChampionSpellAttrData(PyotStatic):
    attribute: str
    modifiers: List[MerakiChampionSpellModifierData]
    affected_by_cdr: bool


class MerakiChampionSpellEffectData(PyotStatic):
    description: str
    leveling: List[MerakiChampionSpellAttrData]


class MerakiChampionSpellData(PyotStatic):
    name: str
    icon: str
    effects: List[MerakiChampionSpellEffectData]
    cost: MerakiChampionSpellAttrData
    cooldown: MerakiChampionSpellAttrData
    targeting: str
    affects: str
    spellshieldable: str
    resource: str
    damage_type: str
    spell_effects: str
    projectile: str
    on_hit_effects: str
    occurrence: int
    notes: str
    blurb: str
    missile_speed: str
    recharge_rate: str
    collision_radius: str
    tether_radius: str
    on_target_cd_static: str
    inner_radius: str
    speed: str
    width: str
    angle: str
    cast_time: str
    effect_radius: str
    target_range: str


class MerakiChampionAbilityData(PyotStatic):
    p: List[MerakiChampionSpellData]
    q: List[MerakiChampionSpellData]
    w: List[MerakiChampionSpellData]
    e: List[MerakiChampionSpellData]
    r: List[MerakiChampionSpellData]


class MerakiChampionAttributeRatingData(PyotStatic):
    damage: int
    toughness: int
    control: int
    mobility: int
    utility: int
    ability_reliance: int
    attack: int
    defense: int
    magic: int
    difficulty: int


class MerakiChampionStatDetailData(PyotStatic):
    flat: float
    percent: float
    per_level: float
    percent_per_level: float


class MerakiChampionStatData(PyotStatic):
    health: MerakiChampionStatDetailData
    health_regen: MerakiChampionStatDetailData
    mana: MerakiChampionStatDetailData
    mana_regen: MerakiChampionStatDetailData
    armor: MerakiChampionStatDetailData
    magic_resistance: MerakiChampionStatDetailData
    attack_damage: MerakiChampionStatDetailData
    movespeed: MerakiChampionStatDetailData
    acquisition_radius: MerakiChampionStatDetailData
    selection_radius: MerakiChampionStatDetailData
    pathing_radius: MerakiChampionStatDetailData
    gameplay_radius: MerakiChampionStatDetailData
    critical_strike_damage: MerakiChampionStatDetailData
    critical_strike_damage_modifier: MerakiChampionStatDetailData
    attack_speed: MerakiChampionStatDetailData
    attack_speed_ratio: MerakiChampionStatDetailData
    attack_cast_time: MerakiChampionStatDetailData
    attack_total_time: MerakiChampionStatDetailData
    attack_delay_offset: MerakiChampionStatDetailData
    attack_range: MerakiChampionStatDetailData
    aram_damage_taken: MerakiChampionStatDetailData
    aram_damage_dealt: MerakiChampionStatDetailData
    aram_healing: MerakiChampionStatDetailData
    aram_shielding: MerakiChampionStatDetailData
    urf_damage_taken: MerakiChampionStatDetailData
    urf_damage_dealt: MerakiChampionStatDetailData
    urf_healing: MerakiChampionStatDetailData
    urf_shielding: MerakiChampionStatDetailData


class MerakiChampionPriceData(PyotStatic):
    blue_essence: int
    rp: int
    sale_rp: int


class MerakiChampionChromaDescriptionsData(PyotStatic):
    region: str = None
    description: str


class MerakiChampionChromaRaritiesData(PyotStatic):
    region: str = None
    description: str
    rarity: int


class MerakiChampionSkinChromaData(PyotStatic):
    id: int
    name: str
    chroma_path: str
    colors: List[str]
    descriptions: List[MerakiChampionChromaDescriptionsData]
    rarities: List[MerakiChampionChromaRaritiesData]

    class Meta(PyotStatic.Meta):
        raws = {"colors"}


class MerakiChampionSkinData(PyotStatic):
    name: str
    id: int
    is_base: bool
    availability: str
    format_name: str
    loot_eligible: bool
    cost: Union[str, int]
    sale: int
    distribution: str
    rarity: str
    chromas: List[MerakiChampionSkinChromaData]
    lore: str
    release: str
    set: List[str]
    splash_path: str
    uncentered_splash_path: str
    tile_path: str
    load_screen_path: str
    load_screen_vintage_path: str
    new_effects: bool
    new_animations: bool
    new_recall: bool
    new_voice: bool
    new_quotes: bool
    voice_actor: List[str]
    splash_artist: List[str]

    class Meta(PyotStatic.Meta):
        raws = {"set", "voice_actor", "splash_artist"}


# PYOT CORE OBJECTS

class MerakiChampion(PyotCore):
    id: int
    key: str
    name: str
    title: str
    full_name: str
    icon: str
    resource: str
    attack_type: str
    adaptive_type: str
    stats: MerakiChampionStatData
    roles: List[str]
    attribute_ratings: MerakiChampionAttributeRatingData
    abilities: MerakiChampionAbilityData
    release_date: str
    release_patch: str
    patch_last_changed: str
    price: MerakiChampionPriceData
    skins: List[MerakiChampionSkinData]
    lore: str

    class Meta(PyotCore.Meta):
        server_type = "locale"
        rules = {"meraki_champion_by_key": ["key"]}
        raws = {"roles"}

    def __init__(self, id: int = None, key: str = None, name: str = None):
        self.initialize({"locale": "default", **locals()})

    async def setup(self):
        if not hasattr(self, "key"):
            if hasattr(self, "id"):
                self.key = await key_by_id(self.id)
            elif hasattr(self, "name"):
                self.key = await key_by_name(self.name)
        if self.key == "FiddleSticks":  # MERAKI HAS LOWERCASE S ON FIDDLE
            self.key = "Fiddlesticks"

    @property
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(key=self.key, locale="en_us")

    def transform(self, data):
        if data["key"] == "Fiddlesticks":  # MERAKI HAS LOWERCASE S ON FIDDLE, GO BACK
            data["key"] = "FiddleSticks"
        return data
