from typing import List, Iterator, Mapping

from pyot.utils.cdragon import tft_item_sanitize, tft_url
from pyot.core.functional import cache_indexes, lazy_property
from .__core__ import PyotCore


# PYOT CORE OBJECT

class Item(PyotCore):
    description: str
    effects: Mapping[str, int]
    from_ids: List[int]
    icon_path: str
    id: int
    name: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["id"]}
        raws = ["from_ids", "effects"]
        renamed = {"from":"from_ids", "desc": "description", "icon": "icon_path"}

    def __init__(self, id: int = None, locale: str = None):
        self._lazy_set(locals())

    @cache_indexes
    def _filter(self, indexer, data):
        return indexer.get(self.id, data["items"], "id")

    def _clean(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"
        self._hide_load_value("id")

    @lazy_property
    def icon_abspath(self) -> str:
        return tft_url(self.icon_path)

    @lazy_property
    def cleaned_description(self):
        return tft_item_sanitize(self.description, self.effects)

    @property
    def from_items(self) -> List["Item"]:
        return [Item(id=i, locale=self.locale) for i in self.from_ids]


class Items(PyotCore):
    items: List[Item]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": []}

    def __init__(self, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.items[item]

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def _clean(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"

    def _filter(self, data):
        return data["items"]

    def _transform(self, data):
        return {"items": data}
