from .__core__ import PyotCore
from pyot.utils.cdragon import tft_item_sanitize, tft_url
from pyot.core.exceptions import NotFound
from typing import List, Iterator, Mapping


# PYOT CORE OBJECT

class Item(PyotCore):
    description: str
    cleaned_description: str
    effects: Mapping[str, int]
    from_ids: List[int]
    icon_path: str
    id: int
    name: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["id"]}
        raws = ["from_ids", "effects"]
        renamed = {"from":"from_ids", "desc": "description"}

    def __init__(self, id: int = None, locale: str = None):
        self._lazy_set(locals())

    def _filter(self, data_):
        data = data_["items"]
        for item in data:
            if item["id"] == self.id:
                return item
        raise NotFound

    def _refactor(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"
        load = getattr(self._meta, "load")
        load.pop("id")

    def _transform(self, data):
        data["iconPath"] = tft_url(data.pop("icon"))
        data["cleanedDescription"] = tft_item_sanitize(data["desc"], data["effects"])
        return data

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

    def _refactor(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"

    def _filter(self, data):
        return data["items"]

    def _transform(self, data):
        return {"items": data}
