from typing import List, Iterator, Dict, Union

from pyot.conf.model import models
from pyot.core.functional import cache_indexes, lazy_property
from pyot.utils.tft.cdragon import sanitize_item, abs_url
from .base import PyotCore


# PYOT CORE OBJECT

class Item(PyotCore):
    description: str
    effects: Dict[str, Union[float, str]]
    from_ids: List[int]
    icon_path: str
    id: int
    name: str
    unique: bool

    class Meta(PyotCore.Meta):
        raws = {"from_ids", "effects"}
        rules = {"cdragon_tft_full": ["?id", "version", "locale"]}
        renamed = {"from":"from_ids", "desc": "description", "icon": "icon_path"}

    def __init__(self, id: int = None, version: str = models.tft.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    @cache_indexes
    def filter(self, indexer, data):
        return indexer.get(self.id, data["items"], "id")

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)

    @lazy_property
    def cleaned_description(self) -> str:
        return sanitize_item(self.description, self.effects)

    @property
    def from_items(self) -> List["Item"]:
        return [Item(id=i, version=self.version, locale=self.locale) for i in self.from_ids]


class Items(PyotCore):
    items: List[Item]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["version", "locale"]}

    def __init__(self, version: str = models.tft.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.items[item]

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def filter(self, data):
        return data["items"]

    def transform(self, data):
        return {"items": data}
