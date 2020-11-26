from .__core__ import PyotStatic, PyotCore
from typing import List


# PYOT STATIC OBJECTS

class MerakiItemStatDetailData(PyotStatic):
    flat: int
    percent: int
    per_level: int
    percent_per_level: int
    percent_base: int
    percent_bonus: int


class MerakiItemStatData(PyotStatic):
    ability_power: MerakiItemStatDetailData
    armor: MerakiItemStatDetailData
    armor_penetration: MerakiItemStatDetailData
    attack_damage: MerakiItemStatDetailData
    attack_speed: MerakiItemStatDetailData
    cooldown_reduction: MerakiItemStatDetailData
    critical_strike_chance: MerakiItemStatDetailData
    gold_per_10: MerakiItemStatDetailData
    heal_and_shield_power: MerakiItemStatDetailData
    health: MerakiItemStatDetailData
    health_regen: MerakiItemStatDetailData
    lethality: MerakiItemStatDetailData
    lifesteal: MerakiItemStatDetailData
    magic_penetration: MerakiItemStatDetailData
    magic_resistance: MerakiItemStatDetailData
    mana: MerakiItemStatDetailData
    mana_regen: MerakiItemStatDetailData
    movespeed: MerakiItemStatDetailData
    ability_haste: MerakiItemStatDetailData
    omnivamp: MerakiItemStatDetailData


class MerakiItemPassiveData(PyotStatic):
    unique: bool
    name: str
    effects: str
    range: int
    stats: MerakiItemStatData


class MerakiItemActiveData(PyotStatic):
    unique: bool
    name: str
    effects: str
    range: int
    cooldown: int


class MerakiItemShopPriceData(PyotStatic):
    total: int
    combined: int
    sell: int


class MerakiItemShopData(PyotStatic):
    prices: MerakiItemShopPriceData
    purchasable: bool
    tags: List[str]

    class Meta(PyotStatic.Meta):
        raws = ["tags"]


# PYOT CORE OBJECTS

class MerakiItem(PyotCore):
    name: str
    id: int
    tier: int
    rank: List[str]
    builds_from_ids: List[int]
    builds_into_ids: List[int]
    no_effects: bool
    removed: bool
    required_champion_key: str
    required_ally: str
    icon: str
    simple_description: str
    nicknames: List[str]
    passives: List[MerakiItemPassiveData]
    active: List[MerakiItemActiveData]
    stats: MerakiItemStatData
    shop: MerakiItemShopData

    class Meta(PyotCore.Meta):
        rules = {"meraki_item_by_id": ["id"]}
        raws = ["builds_from_ids", "builds_into_ids", "nicknames", "rank"]
        renamed = {"builds_from": "builds_from_ids", "builds_into": "builds_into_ids", "required_champion": "required_champion_key"}

    def __init__(self, id: int = None):
        locale = "default"
        self._lazy_set(locals())

    @property
    def item(self) -> "Item":
        from .item import Item
        return Item(id=self.id, locale="en_us") 

    @property
    def meraki_builds_from(self) -> List["MerakiItem"]:
        mutable = []
        for i in self.builds_from_ids:
            mutable.append(MerakiItem(id=i))
        return mutable

    @property
    def meraki_builds_into(self) -> List["MerakiItem"]:
        mutable = []
        for i in self.builds_into_ids:
            mutable.append(MerakiItem(id=i))
        return mutable

    @property
    def builds_from(self) -> List["Item"]:
        from .item import Item
        mutable = []
        for i in self.builds_from_ids:
            mutable.append(Item(id=i, locale="en_us"))
        return mutable

    @property
    def builds_into(self) -> List["Item"]:
        from .item import Item
        mutable = []
        for i in self.builds_into_ids:
            mutable.append(Item(id=i, locale="en_us"))
        return mutable

    @property
    def required_champion(self) -> "Champion":
        from .champion import Champion
        return Champion(id=self.required_champion_key, locale="en_us")

    @property
    def meraki_required_champion(self) -> "MerakiChampion":
        from .merakichampion import MerakiChampion
        return MerakiChampion(id=self.required_champion_key)
