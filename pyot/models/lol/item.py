from typing import List, Iterator, TYPE_CHECKING

from pyot.conf.model import models
from pyot.core.functional import cache_indexes, lazy_property
from pyot.utils.lol.cdragon import abs_url, sanitize
from .base import PyotCore

if TYPE_CHECKING:
    from .merakiitem import MerakiItem


# PYOT CORE OBJECT

class Item(PyotCore):
    id: int
    name: str
    description: str
    active: bool
    in_store: bool
    from_ids: List[int]
    to_ids: List[int]
    categories: List[str]
    maps: List[str]
    max_stacks: int
    modes: List[str]
    required_champion_key: str
    required_ally: str
    required_currency: str
    required_currency_cost: int
    is_enchantment: bool
    special_recipe: int
    self_cost: int
    total_cost: int
    icon_path: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_item_full": ["version", "locale", "?id"]}
        raws = {"from_ids", "to_ids", "categories", "maps", "modes"}
        renamed = {"from":"from_ids", "to": "to_ids", "map_string_id_inclusions": "maps", "mode_name_inclusions": "modes",
            "required_buff_currency_name": "required_currency", "required_buff_currency_cost": "required_currency_cost",
            "price": "self_cost", "price_total": "total_cost"}

    def __init__(self, id: int = None, version: str = models.lol.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    @cache_indexes
    def filter(self, indexer, data):
        return indexer.get(self.id, data, "id")

    def transform(self, data):
        if data["requiredChampion"] == "":
            data["requiredChampion"] = None
        if data["requiredBuffCurrencyName"] == "":
            data["requiredBuffCurrencyName"] = "GOLD"
            data["requiredBuffCurrencyCost"] = data["price"]
        return data

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)

    @lazy_property
    def cleaned_description(self) -> str:
        return sanitize(self.description)

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
        rules = {"cdragon_item_full": ["version", "locale"]}

    def __init__(self, version: str = models.lol.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.items[item]

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def transform(self, data):
        return {"items": data}
