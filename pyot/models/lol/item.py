from .__core__ import PyotCore, PyotStatic
from pyot.utils.cdragon import cdragon_url, cdragon_sanitize
from pyot.core.exceptions import NotFound
from typing import List, Iterator


# PYOT CORE OBJECT

class Item(PyotCore):
    id: int
    name: str
    description: str
    cleaned_description: str
    active: bool
    in_store: bool
    from_ids: List[int]
    to_ids: List[int]
    categories: List[str]
    maps: List[str]
    max_stacks: int
    modes: List[str]
    required_champion_key: str
    required_currency: str
    required_currency_cost: int
    special_recipe: int
    self_cost: int
    total_cost: int
    icon_path: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_item_full": ["id"]}
        raws = ["from_ids", "to_ids", "categories", "maps", "modes"]
        renamed = {"from":"from_ids", "to": "to_ids", "map_string_id_inclusions": "maps", "mode_name_inclusions": "modes",
            "required_buff_currency_name": "required_currency", "required_buff_currency_cost": "required_currency_cost",
            "price": "self_cost", "price_total": "total_cost"}
        removed = ["required_ally", "is_enchantment"]

    def __init__(self, id: int = None, locale: str = None):
        self._lazy_set(locals())

    def filter(self, data):
        for item in data:
            if item["id"] == self.id:
                return item
        raise NotFound

    def _refactor(self):
        if self.locale.lower() == "en_us":
            self.meta.server = "default"
        load = getattr(self.meta, "load")
        load.pop("id")

    def _transform(self, data):
        data["iconPath"] = cdragon_url(data["iconPath"])
        data["cleanedDescription"] = cdragon_sanitize(data["description"])
        if data["requiredChampion"] == "":
            data["requiredChampion"] = None
        if data["requiredBuffCurrencyName"] == "":
            data["requiredBuffCurrencyName"] = "GOLD"
            data["requiredBuffCurrencyCost"] = data["price"]
        return data

    @property
    def from_items(self) -> List["Item"]:
        items = []
        for id in self.from_ids:
            items.append(Item(id=id, locale=self.locale))
        return items

    @property
    def to_items(self) -> List["Item"]:
        items = []
        for id in self.to_ids:
            items.append(Item(id=id, locale=self.locale))
        return items

    @property
    def meraki_item(self) -> "MerakiItem":
        from .merakiitem import MerakiItem
        return MerakiItem(id=self.id)


class Items(PyotCore):
    items: List[Item]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_item_full": []}

    def __init__(self, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def _refactor(self):
        if self.locale.lower() == "en_us":
            self.meta.server = "default"

    def _transform(self, data_):
        items = []
        for data in data_:
            data["iconPath"] = cdragon_url(data["iconPath"])
            data["cleanedDescription"] = cdragon_sanitize(data["description"])
            if data["requiredChampion"] == "":
                data["requiredChampion"] = None
            if data["requiredBuffCurrencyName"] == "":
                data["requiredBuffCurrencyName"] = "GOLD"
                data["requiredBuffCurrencyCost"] = data["price"]
            items.append({"data": data})
        return {"items": items}